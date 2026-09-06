"""Minimal Parquet page-header scanner (thrift compact protocol).

Purpose (Phase 1 - data integrity audit only):
    Map an absolute byte offset inside a Parquet file to the exact
    [row_lo, row_hi) interval of logical rows that straddle that byte offset.

Why this exists:
    The XAUUSD dataset is shipped as 7 byte-split fragments of ONE Parquet
    file.  To audit the seam between fragment N and fragment N+1 we must know
    WHICH rows of the reassembled table are physically cut in half by the
    fragment boundary.  Row-group metadata alone is too coarse; page headers
    give an exact (and conservative) row interval.

No data is modified.  The scanner is read-only.

Thrift compact protocol reference:
    https://github.com/apache/thrift/blob/master/doc/specs/thrift-compact-protocol.md
Parquet PageHeader reference:
    https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------- compact types
T_STOP = 0x00
T_TRUE = 0x01
T_FALSE = 0x02
T_BYTE = 0x03
T_I16 = 0x04
T_I32 = 0x05
T_I64 = 0x06
T_DOUBLE = 0x07
T_BINARY = 0x08
T_LIST = 0x09
T_SET = 0x0A
T_MAP = 0x0B
T_STRUCT = 0x0C


class CompactReader:
    __slots__ = ("buf", "pos")

    def __init__(self, buf: bytes, pos: int = 0) -> None:
        self.buf = buf
        self.pos = pos

    def byte(self) -> int:
        b = self.buf[self.pos]
        self.pos += 1
        return b

    def varint(self) -> int:
        result = 0
        shift = 0
        while True:
            b = self.buf[self.pos]
            self.pos += 1
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                return result
            shift += 7

    def zigzag(self) -> int:
        n = self.varint()
        return (n >> 1) ^ -(n & 1)

    def binary(self) -> bytes:
        n = self.varint()
        out = self.buf[self.pos:self.pos + n]
        self.pos += n
        return out

    def skip(self, ttype: int) -> None:
        r = self
        if ttype in (T_TRUE, T_FALSE, T_STOP):
            return
        if ttype == T_BYTE:
            r.pos += 1
        elif ttype in (T_I16, T_I32, T_I64):
            r.varint()
        elif ttype == T_DOUBLE:
            r.pos += 8
        elif ttype == T_BINARY:
            n = r.varint()
            r.pos += n
        elif ttype in (T_LIST, T_SET):
            head = r.byte()
            size = (head >> 4) & 0x0F
            etype = head & 0x0F
            if size == 15:
                size = r.varint()
            for _ in range(size):
                r.skip(etype)
        elif ttype == T_MAP:
            size = r.varint()
            if size == 0:
                return
            head = r.byte()
            ktype = (head >> 4) & 0x0F
            vtype = head & 0x0F
            for _ in range(size):
                r.skip(ktype)
                r.skip(vtype)
        elif ttype == T_STRUCT:
            r.read_struct()
        else:
            raise ValueError(f"unknown thrift compact type {ttype} at pos {r.pos}")

    def read_struct(self) -> dict[int, Any]:
        """Read a struct, returning {field_id: value}.

        Nested structs / lists are returned as nested dicts / lists only when
        they are cheap; everything else is skipped but still consumed, so the
        stream position stays correct.
        """
        out: dict[int, Any] = {}
        last_fid = 0
        while True:
            head = self.byte()
            if head == T_STOP:
                return out
            ttype = head & 0x0F
            delta = (head >> 4) & 0x0F
            if delta == 0:
                fid = self.zigzag()
            else:
                fid = last_fid + delta
            last_fid = fid
            out[fid] = self._value(ttype)

    def _value(self, ttype: int) -> Any:
        r = self
        if ttype == T_TRUE:
            return True
        if ttype == T_FALSE:
            return False
        if ttype == T_BYTE:
            return r.byte() - ((r.byte() if False else 0))  # i8, unused here
        if ttype in (T_I16, T_I32, T_I64):
            return r.zigzag()
        if ttype == T_DOUBLE:
            import struct

            v = struct.unpack("<d", r.buf[r.pos:r.pos + 8])[0]
            r.pos += 8
            return v
        if ttype == T_BINARY:
            return r.binary()
        if ttype == T_STRUCT:
            return r.read_struct()
        if ttype in (T_LIST, T_SET):
            head = r.byte()
            size = (head >> 4) & 0x0F
            etype = head & 0x0F
            if size == 15:
                size = r.varint()
            items = []
            for _ in range(size):
                items.append(r._value(etype))
            return items
        if ttype == T_MAP:
            size = r.varint()
            items = []
            if size:
                head = r.byte()
                vtype = head & 0x0F
                ktype = (head >> 4) & 0x0F
                for _ in range(size):
                    k = r._value(ktype)
                    v = r._value(vtype)
                    items.append((k, v))
            return items
        raise ValueError(f"unsupported thrift type {ttype}")


# ------------------------------------------------------------------ page model
PAGE_DATA, PAGE_INDEX, PAGE_DICT, PAGE_DATA_V2 = 0, 1, 2, 3


@dataclass
class Page:
    page_index: int
    byte_start: int          # first byte of the page header
    data_start: int          # first byte of compressed page payload
    data_end: int            # one past last byte of compressed page payload
    header_len: int
    page_type: int
    compressed_size: int
    uncompressed_size: int
    num_values: int          # 0 for dictionary pages (rows are counted separately)

    @property
    def type_name(self) -> str:
        return {0: "DATA_PAGE", 1: "INDEX_PAGE", 2: "DICTIONARY_PAGE",
                3: "DATA_PAGE_V2"}.get(self.page_type, f"UNKNOWN({self.page_type})")


@dataclass
class ColumnChunkScan:
    row_group: int
    column: str
    chunk_start: int
    chunk_end: int
    pages: list[Page] = field(default_factory=list)

    def rows_before_page(self, page_index: int) -> int:
        """Number of logical rows stored in DATA pages before `page_index`."""
        return sum(p.num_values for p in self.pages[:page_index]
                   if p.page_type in (PAGE_DATA, PAGE_DATA_V2))


def scan_column_chunk(path: str, row_group: int, column: str,
                      chunk_start: int, total_compressed_size: int,
                      read_size: int = 0) -> ColumnChunkScan:
    """Sequentially parse every PageHeader of one column chunk."""
    scan = ColumnChunkScan(row_group, column, chunk_start,
                           chunk_start + total_compressed_size)
    with open(path, "rb") as fh:
        fh.seek(chunk_start)
        # page headers are small; read the whole chunk header region lazily
        buf = fh.read(total_compressed_size + 1)
    r = CompactReader(buf, 0)
    pos = 0
    idx = 0
    while pos < total_compressed_size:
        r.pos = pos
        header = r.read_struct()
        header_len = r.pos - pos
        ptype = header.get(1, -1)
        uncompressed = header.get(2, 0)
        compressed = header.get(3, 0)
        num_values = 0
        if ptype in (PAGE_DATA, PAGE_DATA_V2):
            dph = header.get(5 if ptype == PAGE_DATA else 8, {}) or {}
            num_values = dph.get(1, 0)
        elif ptype == PAGE_DICT:
            dph = header.get(7, {}) or {}
            num_values = dph.get(1, 0)  # dictionary size, NOT row count
        scan.pages.append(Page(
            page_index=idx,
            byte_start=chunk_start + pos,
            data_start=chunk_start + pos + header_len,
            data_end=chunk_start + pos + header_len + compressed,
            header_len=header_len,
            page_type=ptype,
            compressed_size=compressed,
            uncompressed_size=uncompressed,
            num_values=num_values if ptype in (PAGE_DATA, PAGE_DATA_V2) else 0,
        ))
        pos += header_len + compressed
        idx += 1
        if compressed == 0:
            break
    return scan


def locate_byte_offset(scans: dict[tuple[int, str], ColumnChunkScan],
                       rg_offsets: dict[int, int],
                       offset: int) -> dict:
    """Map an absolute file byte offset to a conservative row interval."""
    # 1. find the chunk containing the offset
    best = None
    for (rg, col), scan in scans.items():
        if scan.chunk_start <= offset < scan.chunk_end:
            best = scan
            break
    if best is None:
        return {"found": False, "offset": offset}
    # 2. find the page containing the offset
    page = None
    for p in best.pages:
        if p.byte_start <= offset < p.data_end:
            page = p
            break
    if page is None:
        return {"found": False, "offset": offset, "chunk": f"rg{best.row_group}/{best.column}"}
    rows_before = best.rows_before_page(page.page_index)
    if page.page_type in (PAGE_DATA, PAGE_DATA_V2):
        frac = (offset - page.data_start) / max(1, (page.data_end - page.data_start))
        est = rows_before + int(frac * page.num_values)
        row_lo = rows_before
        row_hi = rows_before + page.num_values
    else:
        # boundary lands on a dictionary page: no rows are cut here
        frac = (offset - page.data_start) / max(1, (page.data_end - page.data_start))
        est = rows_before
        row_lo = rows_before
        row_hi = rows_before
    base = rg_offsets.get(best.row_group, 0)
    return {
        "found": True,
        "offset": offset,
        "row_group": best.row_group,
        "column": best.column,
        "page_index": page.page_index,
        "page_type": page.type_name,
        "page_bytes": page.compressed_size,
        "page_num_values": page.num_values,
        "fraction_in_page": round(frac, 6),
        "row_lo_rg": row_lo,
        "row_hi_rg": row_hi,
        "row_estimate_rg": est,
        "row_lo_global": base + row_lo,
        "row_hi_global": base + row_hi,
        "row_estimate_global": base + est,
        "interval_width_rows": row_hi - row_lo,
    }
