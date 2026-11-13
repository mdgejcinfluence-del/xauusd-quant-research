"""Inventaire exhaustif LECTURE SEULE des 348 partitions.
Footers Parquet uniquement (requetes Range HTTP): aucune ligne de donnees,
aucun telechargement complet, aucune ecriture sur Drive, aucune conversion."""
import io, json, re, hashlib, pathlib, time
import requests
import pyarrow.parquet as pq

FOLDER = "1gQc_VjKSTDLzRZZa6B8mO071nf8XG28e"
S = requests.Session(); S.headers.update({"User-Agent":"Mozilla/5.0"})

def listing():
    html = S.get(f"https://drive.google.com/embeddedfolderview?id={FOLDER}#list", timeout=60).text
    pairs = [(num, fid) for fid, num in re.findall(
        r'href="https://drive\.google\.com/file/d/([A-Za-z0-9_-]+)[^"]*"[^>]*>(?:(?!</a>).)*?part_(\d{6})\.parquet', html, re.S)]
    out = {f"part_{num}.parquet": fid for num, fid in pairs}
    if len(out) != 348: raise RuntimeError(f"listing: {len(out)} partitions (348 attendues)")
    return dict(sorted(out.items()))

class RangeFile(io.RawIOBase):
    def __init__(self, fid):
        self.url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
        self.pos = 0; self._size = None
    @property
    def size(self):
        if self._size is None:
            r = S.get(self.url, headers={"Range":"bytes=0-0"}, timeout=60)
            cr = r.headers.get("Content-Range","")
            if "/" not in cr: raise RuntimeError(f"range non supporte HTTP {r.status_code}")
            self._size = int(cr.rsplit("/",1)[1])
        return self._size
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence==0 else self.pos+off if whence==1 else self.size+off
        return self.pos
    def read(self, n=-1):
        if n is None or n<0: n = self.size-self.pos
        if n==0: return b""
        end = self.pos+n-1; last_err=None
        for attempt in range(5):
            try:
                r = S.get(self.url, headers={"Range":f"bytes={self.pos}-{end}"}, timeout=120)
                if r.status_code == 206: data = r.content[:n]
                elif r.status_code == 200: data = r.content[self.pos:self.pos+n]
                else: raise RuntimeError(f"range HTTP {r.status_code} @{self.pos}")
                self.pos += len(data); return data
            except Exception as e:
                last_err=e; time.sleep(2*(attempt+1))
        raise RuntimeError(f"range echec apres 5 essais: {last_err}")

def col_stats(pf, wanted):
    """Min/max footer de la colonne `wanted`, agreges sur les row groups."""
    idx = pf.schema_arrow.names.index(wanted) if wanted in pf.schema_arrow.names else None
    if idx is None: return None, None, None
    mn = mx = None; nulls = 0
    for g in range(pf.metadata.num_row_groups):
        st = pf.metadata.row_group(g).column(idx).statistics
        if st is None: continue
        if st.min is not None: mn = st.min if (mn is None or st.min < mn) else mn
        if st.max is not None: mx = st.max if (mx is None or st.max > mx) else mx
        nulls += (st.null_count or 0)
    fmt = lambda v: v.isoformat() if hasattr(v, "isoformat") else v
    return fmt(mn), fmt(mx), nulls

def main():
    lst = listing()
    out = {"folder_id": FOLDER, "read_only": True, "partitions": [], "errors": []}
    sigs = {}
    for name, fid in lst.items():
        try:
            rf = RangeFile(fid); pf = pq.ParquetFile(rf); md = pf.metadata
            cols = [(pf.schema_arrow.names[i], str(pf.schema_arrow.types[i])) for i in range(len(pf.schema_arrow.names))]
            sig = hashlib.sha256("|".join(f"{a}:{b}" for a,b in cols).encode()).hexdigest()[:16]
            e = sigs.setdefault(sig, {"columns": cols, "count": 0, "rows": 0, "first": name, "last": name})
            e["count"] += 1; e["rows"] += md.num_rows; e["last"] = name
            tmin, tmax, tnull = col_stats(pf, "timestamp_utc")
            omin, omax, onull = col_stats(pf, "observation_id")
            out["partitions"].append({"name": name, "drive_id": fid, "file_bytes": rf.size,
                "rows": md.num_rows, "row_groups": md.num_row_groups,
                "created_by": md.created_by, "schema_signature": sig,
                "timestamp_min_footer": tmin, "timestamp_max_footer": tmax, "timestamp_nulls_footer": tnull,
                "observation_id_min_footer": omin, "observation_id_max_footer": omax, "observation_id_nulls_footer": onull})
        except Exception as ex:
            out["errors"].append({"name": name, "drive_id": fid, "error": f"{type(ex).__name__}: {ex}"})
        if len(out["partitions"]) % 50 == 0: print(f"{len(out['partitions'])} ok", flush=True)
    out["total_rows"] = sum(p["rows"] for p in out["partitions"])
    out["schema_signatures"] = sigs
    out["partitions_sha256_listing"] = "sha256:" + hashlib.sha256("|".join(sorted(lst)).encode()).hexdigest()
    pathlib.Path("reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"ok": len(out["partitions"]), "errors": len(out["errors"]), "total": out["total_rows"]}, indent=1))

if __name__ == "__main__": main()
