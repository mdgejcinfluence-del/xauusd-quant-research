"""Accès DuckDB borné.

Une seule façon d'ouvrir la base : avec une limite de mémoire et un
répertoire de spill explicites. Refuser une connexion non bornée est
volontaire : c'est la garantie qu'aucun code ne chargera 685 M de lignes
en mémoire par inadvertance.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import duckdb


class UnboundedConnectionError(RuntimeError):
    pass


@contextmanager
def connect(
    memory_limit: str = "4GB",
    threads: int = 2,
    temp_dir: str | os.PathLike[str] = "/tmp/duckdb_spill",
    read_only: bool = False,
    database: str = ":memory:",
) -> Iterator[duckdb.DuckDBPyConnection]:
    if not memory_limit:
        raise UnboundedConnectionError("memory_limit obligatoire (aucune connexion non bornée)")
    if threads < 1:
        raise UnboundedConnectionError("threads doit être >= 1")

    tmp = Path(temp_dir)
    tmp.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(database=database, read_only=read_only)
    try:
        con.execute(f"SET memory_limit='{memory_limit}'")
        con.execute(f"SET threads={int(threads)}")
        con.execute(f"SET temp_directory='{tmp.as_posix()}'")
        con.execute("SET preserve_insertion_order=false")
        yield con
    finally:
        con.close()


def describe_parquet(path: str | os.PathLike[str]) -> dict:
    """Schéma + métadonnées d'une partition. Lecture des seules métadonnées.

    On interroge le footer Parquet via pyarrow (fiable, aucun chargement de
    données) et on complète avec les types DuckDB pour rester cohérent avec
    le moteur de calcul.
    """
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(str(path))
    arrow_schema = pf.schema_arrow
    with connect(memory_limit="1GB", threads=1) as con:
        duck_types = {
            r[0]: r[1]
            for r in con.execute(
                "SELECT name, type FROM parquet_schema(?)", [str(path)]
            ).fetchall()
            if r[0] and r[1] is not None
        }
    return {
        "path": str(path),
        "size_bytes": Path(path).stat().st_size,
        "columns": [
            {"name": f.name, "arrow_type": str(f.type), "duckdb_type": duck_types.get(f.name)}
            for f in arrow_schema
        ],
        "num_columns": arrow_schema.__len__(),
        "num_rows": int(pf.metadata.num_rows),
        "num_row_groups": int(pf.metadata.num_row_groups),
        "created_by": pf.metadata.created_by,
    }
