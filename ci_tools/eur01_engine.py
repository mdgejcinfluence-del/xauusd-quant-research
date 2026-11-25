#!/usr/bin/env python3
"""EUR-EDGE-01 — Socle de donnees EUR/USD.
Modes:
  probe : echantillon technique Dukascopy EURUSD (1 journee recente complete + 1 heure 2010),
          QC complet, barres derivees M1..D1, estimation de taille. ECHANTILLON LIMITE:
          les conditions Dukascopy interdisent base de donnees/redistribution sans accord
          ecrit -> aucun telechargement massif, aucun transfert Kaggle de ces ticks.
  cot   : CFTC officiel, marche EURO FX code 099741 (Disaggregated futures-only), 2010-2026.
  rates : taux BCE/Fed par sources officielles tentees une a une (statut journalise).
"""
import io, json, lzma, pathlib, struct, sys, urllib.request, zipfile
import numpy as np
import pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
OUT = RACINE / 'research' / 'EUR-EDGE-01'
DONNEES = OUT / 'data'
UA = {'User-Agent': 'Mozilla/5.0 META-ALPHA-research'}


def fetch(url, timeout=90):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def heure_eurusd(h: pd.Timestamp) -> pd.DataFrame | None:
    u = f'https://datafeed.dukascopy.com/datafeed/EURUSD/{h.year}/{h.month - 1:02d}/{h.day:02d}/{h.hour:02d}h_ticks.bi5'
    try:
        brut = fetch(u, 60)
    except Exception as e:
        print(f'  {h} INDISPONIBLE ({type(e).__name__}: {e})')
        return None
    if not brut:
        return None
    dec = lzma.decompress(brut)
    n = len(dec) // 20
    arr = np.frombuffer(dec[:n * 20], dtype='>u4').reshape(n, 5)
    base = np.datetime64(h.tz_localize(None), 'ms')
    return pd.DataFrame({'ts': base + arr[:, 0].astype(np.int64).astype('timedelta64[ms]'),
                         'ask': arr[:, 1] / 100000.0, 'bid': arr[:, 2] / 100000.0})


def qc_ticks(df, nom):
    sp = df.ask - df.bid
    ecarts = df.ts.diff().dt.total_seconds()
    return {'echantillon': nom, 'ticks': int(len(df)), 'debut': str(df.ts.min()), 'fin': str(df.ts.max()),
            'viol_bid_ge_ask': int((df.bid >= df.ask).sum()), 'prix_nonpositifs': int(((df.bid <= 0) | (df.ask <= 0)).sum()),
            'ts_croissants': bool(df.ts.is_monotonic_increasing), 'doublons_ts': int(df.ts.duplicated().sum()),
            'spread_med_pips': round(float(sp.median()) * 10000, 3), 'spread_p95_pips': round(float(sp.quantile(.95)) * 10000, 3),
            'spread_max_pips': round(float(sp.max()) * 10000, 2), 'ecart_max_s': float(ecarts.max()),
            'saut_max_bp': round(float((np.log(df.bid).diff().abs()).max()) * 10000, 2)}


def barres(df, freq):
    t = df.copy()
    t['mid'] = (t.bid + t.ask) / 2
    t['b'] = t.ts.dt.floor(freq)
    g = t.groupby('b').mid
    return pd.DataFrame({'open': g.first(), 'high': g.max(), 'low': g.min(), 'close': g.last(), 'n_ticks': g.size()})


def mode_probe():
    DONNEES.mkdir(parents=True, exist_ok=True)
    jour = pd.Timestamp('2026-11-11')  # mercredi, recul suffisant pour publication complete
    morceaux, rapports = [], []
    import time as _t
    for hh in [0, 6, 8, 13, 16, 21]:
        df = None
        for essai in range(3):
            df = heure_eurusd(jour + pd.Timedelta(hours=hh))
            if df is not None and len(df): break
            _t.sleep(20)
        if df is not None and len(df):
            morceaux.append(df)
    if morceaux:
        T = pd.concat(morceaux).sort_values('ts')
        rapports.append(qc_ticks(T, 'EURUSD 2026-11-11 heures echantillon 00/06/08/13/16/21'))
        taille = {'ticks_jour': int(len(T)), 'octets_parquet_estimes_par_jour': None}
        p = DONNEES / 'echantillon_ticks_2026-11-11.parquet'
        T.to_parquet(p, index=False)
        taille['octets_parquet_estimes_par_jour'] = p.stat().st_size
        taille['estimation_GB_par_an_250j'] = round(p.stat().st_size * 250 / 1e9, 2)
        taille['estimation_GB_2010_2026'] = round(p.stat().st_size * 250 * 17 / 1e9, 1)
        for freq, nom in [('1min', 'M1'), ('5min', 'M5'), ('15min', 'M15'), ('30min', 'M30'), ('1h', 'H1'), ('4h', 'H4')]:
            B = barres(T, freq)
            B.to_parquet(DONNEES / f'echantillon_barres_{nom}_2026-11-11.parquet')
            rapports.append({'barres': nom, 'n': int(len(B))})
        (OUT / 'PROBE_TAILLES.json').write_text(json.dumps(taille, indent=1))
        print(taille)
    import time as _t; _t.sleep(10)
    vieux = heure_eurusd(pd.Timestamp('2015-06-15 10:00'))
    if vieux is not None and len(vieux):
        rapports.append(qc_ticks(vieux, 'EURUSD 2015-06-15 10h (heure temoin historique)'))
    (OUT / 'PROBE_QC.json').write_text(json.dumps(rapports, indent=1, default=str))
    print(json.dumps(rapports, indent=1, default=str))


def mode_cot():
    DONNEES.mkdir(parents=True, exist_ok=True)
    frames, log = [], []
    for an in range(2010, 2027):
        ok = False
        for base in (f'https://www.cftc.gov/files/dea/history/fut_fin_txt_{an}.zip',):  # TFF: l Euro FX est un futur financier, absent du Disaggregated (matieres physiques)
            try:
                brut = fetch(base, 120)
                z = zipfile.ZipFile(io.BytesIO(brut))
                nom = z.namelist()[0]
                d = pd.read_csv(z.open(nom), low_memory=False)
                col_code = [c for c in d.columns if c.strip() == 'CFTC_Contract_Market_Code'] or [c for c in d.columns if 'CFTC_Contract_Market_Code' in c]
                col_nom = [c for c in d.columns if 'Market_and_Exchange' in c]
                if an == 2015:
                    log.append('DIAG colonnes: ' + ' | '.join(map(str, d.columns[:14])))
                    if col_code: log.append('DIAG codes uniques: ' + str(d[col_code[0]].astype(str).str.strip().str.zfill(6).unique()[:12]))
                m = d[(d[col_code[0]].astype(str).str.strip().str.zfill(6) == '099741')] if col_code else d.iloc[0:0]
                if len(m) == 0 and col_nom:
                    m = d[d[col_nom[0]].astype(str).str.contains('EURO FX', na=False)]
                log.append(f'COT {an}: {len(m)} lignes EURO FX 099741')
                if len(m):
                    frames.append(m)
                ok = True
                break
            except Exception as e:
                log.append(f'COT {an}: echec ({type(e).__name__})')
        if not ok:
            pass
    if frames:
        C = pd.concat(frames, ignore_index=True)
        C.to_parquet(DONNEES / 'CFTC_COT_EUROFX_099741_TFF_brut.parquet', index=False)
        log.append(f'COT total brut: {len(C)} lignes, colonnes: {len(C.columns)}')
    (OUT / 'COT_LOG.txt').write_text('\n'.join(log))
    print('\n'.join(log))


def mode_rates():
    DONNEES.mkdir(parents=True, exist_ok=True)
    essais = {
        'ECB_SDMX_DFR': 'https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.DFR.LEV?startPeriod=2010-01-01&format=csvdata',
        'ECB_SDMX_MRO': 'https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_MBR.LEV?startPeriod=2010-01-01&format=csvdata',
        'DBNOMICS_FRED_DEXUSEU': 'https://api.db.nomics.world/v22/series/FRED/DEXUSEU?observations=1',
        'FED_H15_DAILY': 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=c5d8264962a56d48f89f462d8471faab&lastobs=5&filetype=csv&label=include&layout=seriescolumn',
        'DBNOMICS_DEXUSEU': 'https://api.db.nomics.world/v22/series/FRED/DEXUSEU/DEXUSEU?observations=1&format=json',
        'DBNOMICS_DGS10': 'https://api.db.nomics.world/v22/series/FRED/DGS10/DGS10?observations=1&format=json',
        'FRED_DEXUSEU': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU&cosd=2010-01-01',
        'USTREASURY_DAILY': 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611',
    }
    statut = {}
    for nom, url in essais.items():
        try:
            brut = fetch(url, 90)
            (DONNEES / f'rates_{nom}.csv').write_bytes(brut)
            statut[nom] = f'OK {len(brut)} octets'
        except Exception as e:
            statut[nom] = f'ECHEC {type(e).__name__}: {e}'
        print(nom, statut[nom])
    (OUT / 'RATES_LOG.json').write_text(json.dumps(statut, indent=1))


def mode_cotdiag():
    brut = fetch('https://www.cftc.gov/files/dea/history/fut_disagg_txt_2020.zip', 120)
    z = zipfile.ZipFile(io.BytesIO(brut))
    d = pd.read_csv(z.open(z.namelist()[0]), low_memory=False)
    print('fichiers zip:', z.namelist())
    noms = [c for c in d.columns if 'Market_and_Exchange' in c][0]
    tous = sorted(d[noms].astype(str).unique())
    print('marches contenant EUR:', [x for x in tous if 'EUR' in x.upper()][:20])
    print('nb marches:', len(tous), '| lignes:', len(d))
    m = d[d[noms].astype(str).str.contains('EURO FX', na=False)]
    print('lignes EURO FX:', len(m))
    for c in ['CFTC_Contract_Market_Code', 'CFTC_Market_Code', 'CFTC_Commodity_Code']:
        print(c, '->', m[c].astype(str).str.strip().unique()[:5] if c in d.columns else 'ABSENTE')
    print('noms:', m[noms].astype(str).unique()[:5])




def mode_rates2():
    """Completion taux: Bund (Bundesbank), H.15 Fed, Tresor parse, BCE MRO cle alternative."""
    DONNEES.mkdir(parents=True, exist_ok=True)
    essais = {
        'BUNDESBANK_10Y': 'https://api.statistiken.bundesbank.de/rest/data/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R10XX.R.A.A._Z._Z.A?startPeriod=2010-01&format=csv',
        'FED_H15_CSV': 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=c5d8264962a56d48f89f462d8471faab&lastobs=5&filetype=csv&label=include&layout=seriescolumn',
        'ECB_MRO2': 'https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_MBR.LEV?format=csvdata',
        'DBNOMICS_ALFRED_CPI': 'https://api.db.nomics.world/v22/series/ALFRED/CPIAUCNS?observations=1',
        'FRED_MIRROR_DGS10_GH': 'https://raw.githubusercontent.com/datasets/fred/master/data/DGS10.csv',
    }
    statut = {}
    for nom, url in essais.items():
        try:
            brut = fetch(url, 90)
            (DONNEES / f'rates2_{nom}.csv').write_bytes(brut)
            statut[nom] = f'OK {len(brut)} octets, debut: {brut[:80]!r}'
        except Exception as e:
            statut[nom] = f'ECHEC {type(e).__name__}: {e}'
        print(nom, statut[nom])
    (OUT / 'RATES2_LOG.json').write_text(json.dumps(statut, indent=1))


def mode_macro():
    """Vintages/publications officielles: BLS (CPI), Eurostat (HICP) — valeurs et dates reelles.
    Aucun consensus. Les premieres valeurs BLS/Eurostat exigeant des archives de parution,
    chaque ligne porte sa source et son mode d'obtention."""
    DONNEES.mkdir(parents=True, exist_ok=True)
    statut = {}
    # BLS API publique sans cle (limites: fenetres de 10 ans)
    for serie in ('CPIAUCNS', 'CPILFESL', 'PAYEMS', 'UNRATE'):
        morceaux = []
        for a0, a1 in ((2010, 2019), (2020, 2026)):
            try:
                brut = fetch(f'https://api.bls.gov/publicAPI/v2/timeseries/data/{serie}?startyear={a0}&endyear={a1}', 90)
                d = json.loads(brut)
                for x in d['Results']['series'][0]['data']:
                    morceaux.append({'serie': serie, 'annee': int(x['year']), 'periode': x['period'],
                                     'valeur': float(x['value']), 'source': 'BLS public API (valeur courante, revisee le cas echeant)'})
                statut[f'BLS_{serie}_{a0}'] = 'OK'
            except Exception as e:
                statut[f'BLS_{serie}_{a0}'] = f'ECHEC {type(e).__name__}: {e}'
        if morceaux:
            pd.DataFrame(morceaux).to_csv(DONNEES / f'macro_BLS_{serie}.csv', index=False)
    # Eurostat HICP zone euro (indice mensuel)
    try:
        brut = fetch('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_midx?format=JSON&lang=EN&geo=EA20&coicop=CP00&unit=I15&sinceTimePeriod=2010-01', 120)
        (DONNEES / 'macro_EUROSTAT_HICP_raw.json').write_bytes(brut)
        statut['EUROSTAT_HICP'] = f'OK {len(brut)} octets'
    except Exception as e:
        statut['EUROSTAT_HICP'] = f'ECHEC {type(e).__name__}: {e}'
    (OUT / 'MACRO_LOG.json').write_text(json.dumps(statut, indent=1))
    print(json.dumps(statut, indent=1))


if __name__ == '__main__':
    {'probe': mode_probe, 'cot': mode_cot, 'rates': mode_rates, 'cotdiag': mode_cotdiag, 'rates2': mode_rates2, 'macro': mode_macro}[sys.argv[1]]()
