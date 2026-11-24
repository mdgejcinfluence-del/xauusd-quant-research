#!/usr/bin/env python3
"""MA-EDGE-02 — Connecteur Dukascopy (flux public historique, sans compte ni cle).
Source: https://datafeed.dukascopy.com/datafeed/XAUUSD/{AAAA}/{MM-1}/{JJ}/{HH}h_ticks.bi5
Fichiers horaires .bi5 (LZMA) de records big-endian 20 octets:
  int32 decalage_ms, int32 ask*1000, int32 bid*1000, float32 vol_ask, float32 vol_bid.
Aucune donnee n'est redistribuee hors depot de recherche; usage recherche uniquement,
conforme a l'acces public documente. Modes: probe | collect DEBUT_HEURE FIN_HEURE.
"""
import io, json, lzma, pathlib, struct, sys, urllib.request
import numpy as np
import pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
SORTIE = RACINE / 'research' / 'MA-EDGE-02' / 'data'
URL = 'https://datafeed.dukascopy.com/datafeed/XAUUSD/{a}/{m:02d}/{j:02d}/{h:02d}h_ticks.bi5'


def telecharger_heure(h: pd.Timestamp) -> pd.DataFrame | None:
    u = URL.format(a=h.year, m=h.month - 1, j=h.day, h=h.hour)
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 META-ALPHA-research'}), timeout=60) as r:
            brut = r.read()
    except Exception as e:
        print(f'  {h} INDISPONIBLE ({type(e).__name__}: {e}) URL={u}')
        return None
    if not brut:
        return None
    try:
        dec = lzma.decompress(brut)
    except Exception:
        print(f'  {h} LZMA illisible ({len(brut)} octets)')
        return None
    n = len(dec) // 20
    arr = np.frombuffer(dec[:n * 20], dtype='>u4').reshape(n, 5)
    ms = arr[:, 0].astype(np.int64)
    ask = arr[:, 1].astype(np.float64) / 1000.0
    bid = arr[:, 2].astype(np.float64) / 1000.0
    base = np.datetime64(h.tz_localize(None), 'ms')
    ts = base + ms.astype('timedelta64[ms]')
    return pd.DataFrame({'ts': ts, 'bid': bid, 'ask': ask})


def qualite(df: pd.DataFrame) -> dict:
    if df is None or len(df) == 0:
        return {'ticks': 0}
    sp = (df.ask - df.bid) * 100.0  # en bp relatifs approx (prix ~4000-5000: 1 unite = ~2 bp)
    ecarts = df.ts.diff().dt.total_seconds()
    return {'ticks': int(len(df)), 'bid_lt_ask_violations': int((df.bid >= df.ask).sum()),
            'ts_croissants': bool(df.ts.is_monotonic_increasing),
            'spread_mediane_unites': float((df.ask - df.bid).median()),
            'spread_p95_unites': float((df.ask - df.bid).quantile(.95)),
            'ecart_max_sec': float(ecarts.max()) if len(df) > 1 else None,
            'premier': str(df.ts.iloc[0]), 'dernier': str(df.ts.iloc[-1])}


def mode_probe():
    now = pd.Timestamp.utcnow().floor('h')
    res = {}
    for delta in (2, 3, 26, 50):
        h = (now - pd.Timedelta(hours=delta)).floor('h')
        df = telecharger_heure(h)
        res[str(h)] = qualite(df)
        print(h, res[str(h)])
    out = RACINE / 'research' / 'MA-EDGE-02' / 'DUKASCOPY_PROBE.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print('probe ecrite:', out)


def mode_collect(debut: str, fin: str):
    SORTIE.mkdir(parents=True, exist_ok=True)
    man_p = SORTIE / 'COLLECT_MANIFEST.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    heures = pd.date_range(pd.Timestamp(debut), pd.Timestamp(fin), freq='h')
    par_jour = {}
    for h in heures:
        cle = str(h)
        if cle in man:
            continue
        df = telecharger_heure(h)
        if df is None or len(df) == 0:
            # une heure recente peut n'etre pas encore publiee (503): ne jamais la
            # marquer definitivement; seuls les vides anciens (>48 h) sont figes
            if h < pd.Timestamp.now(tz='UTC').tz_localize(None) - pd.Timedelta(hours=48):
                man[cle] = {'ticks': 0, 'statut': 'VIDE_ANCIEN_FIGE'}
            continue
        man[cle] = {'ticks': int(len(df)), 'statut': 'OK', **{k: v for k, v in qualite(df).items() if k in ('bid_lt_ask_violations', 'ts_croissants')}}
        par_jour.setdefault(str(h.date()), []).append(df)
    for jour, morceaux in par_jour.items():
        p = SORTIE / f'duka_{jour}.parquet'
        neuf = pd.concat(morceaux)
        if p.exists():
            neuf = pd.concat([pd.read_parquet(p), neuf])
        neuf = neuf.drop_duplicates('ts').sort_values('ts')
        neuf.to_parquet(p, index=False)
        print(jour, len(neuf), 'ticks cumules')
    man_p.write_text(json.dumps(man, indent=1))
    print('manifeste:', len(man), 'heures tracees')


if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        mode_probe()
    elif sys.argv[1] == 'collect':
        mode_collect(sys.argv[2], sys.argv[3])
