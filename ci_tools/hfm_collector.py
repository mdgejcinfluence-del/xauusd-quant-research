#!/usr/bin/env python3
"""HFM-NATIVE-DATA — collecteur XAUUSD natif HFM via MetaTrader 5 (lecture seule).

Modes:
  probe    : connexion, specs symbole, profondeur reelle (premier tick/barre par TF)
  pilot    : petit lot (7 jours ticks + barres) -> raw/ + normalized/ + qualite
  collect  : plages mensuelles ticks + barres, reprise via COLLECTION_MANIFEST.json
  selftest : pipeline complet sur donnees SYNTHETIQUES (jamais HFM, jamais publie)

Secrets uniquement par environnement: HFM_LOGIN, HFM_PASSWORD, HFM_SERVER, MT5_PATH.
Aucun ordre, aucune ecriture compte: API MT5 en lecture (initialize + copy_*).
MetaTrader5 exige Windows + terminal MT5 installe et connecte au serveur HFM.
"""
import hashlib, json, os, pathlib, sys
import numpy as np, pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
BASE = RACINE / 'research' / 'HFM-NATIVE-DATA'
TF = {'M1':'TIMEFRAME_M1','M5':'TIMEFRAME_M5','M15':'TIMEFRAME_M15','M30':'TIMEFRAME_M30',
      'H1':'TIMEFRAME_H1','H4':'TIMEFRAME_H4','D1':'TIMEFRAME_D1'}
SYMBOLE_DEFAUT = 'XAUUSD'

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def mt5_connect():
    login = os.environ.get('HFM_LOGIN'); pw = os.environ.get('HFM_PASSWORD')
    server = os.environ.get('HFM_SERVER')
    if not (login and pw and server):
        raise SystemExit('BLOCAGE_IDENTIFIANTS: HFM_LOGIN/HFM_PASSWORD/HFM_SERVER absents de l environnement. Aucun identifiant invente, aucune collecte tentee.')
    try:
        import MetaTrader5 as mt5
    except ImportError:
        raise SystemExit('BLOCAGE_PLATEFORME: le package MetaTrader5 exige Windows + terminal MT5 installe connecte a HFM; cet environnement est Linux sans terminal.')
    kw = dict(login=int(login), password=pw, server=server)
    if os.environ.get('MT5_PATH'): kw['path'] = os.environ['MT5_PATH']
    if not mt5.initialize(**kw):
        raise SystemExit(f'MT5 initialize a echoue: {mt5.last_error()}')
    return mt5

def specs(mt5, sym):
    info = mt5.symbol_info(sym)
    if info is None: raise SystemExit(f'Symbole {sym} introuvable sur ce serveur.')
    mt5.symbol_select(sym, True)
    d = info._asdict()
    cles = ['name','description','currency_base','currency_profit','contract_size','volume_min',
            'volume_step','volume_max','trade_tick_size','trade_tick_value','digits','point',
            'spread','trade_mode','filling_mode','swap_mode','swap_long','swap_short']
    return {k: d.get(k) for k in cles}

def mode_probe():
    mt5 = mt5_connect(); sym = os.environ.get('HFM_SYMBOL', SYMBOLE_DEFAUT)
    s = specs(mt5, sym)
    out = {'symbole': sym, 'specs_serveur': s, 'profondeur': {}}
    epoch = pd.Timestamp('2010-01-04', tz='UTC')
    for nom, tf in TF.items():
        r = mt5.copy_rates_range(sym, getattr(mt5, tf), epoch.to_pydatetime(),
                                 pd.Timestamp('2010-02-01', tz='UTC').to_pydatetime())
        out['profondeur'][nom] = None if r is None or len(r)==0 else str(pd.to_datetime(r[0]['time'], unit='s', utc=True))
    t = mt5.copy_ticks_range(sym, epoch.to_pydatetime(),
                             pd.Timestamp('2010-01-11', tz='UTC').to_pydatetime(),
                             mt5.COPY_TICKS_ALL)
    out['profondeur']['TICKS'] = None if t is None or len(t)==0 else str(pd.to_datetime(t[0]['time_msc'], unit='ms', utc=True))
    (BASE/'audits'/'acquisition_audit.json').write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str)); mt5.shutdown()

def qualite_ticks(df):
    if df is None or len(df)==0: return {'ticks':0}
    return {'ticks': int(len(df)),
            'bid_ask_presents': int((df.bid.notna() & df.ask.notna()).sum()),
            'bid_ge_ask': int((df.bid >= df.ask).sum()),
            'doublons_exacts': int(df.duplicated(subset=['time_msc','bid','ask']).sum()),
            'ts_monotones': bool(df.time_msc.is_monotonic_increasing),
            'premier_utc': str(df.ts_utc.iloc[0]), 'dernier_utc': str(df.ts_utc.iloc[-1]),
            'spread_med_usd': float((df.ask-df.bid).median())}

def normaliser_ticks(brut, source_id):
    df = pd.DataFrame(brut)
    df['ts_utc'] = pd.to_datetime(df['time_msc'], unit='ms', utc=True)
    df['available_at_utc'] = df['ts_utc']
    df['source_id'] = source_id
    df['spread'] = df['ask'] - df['bid']
    return df.sort_values('time_msc').reset_index(drop=True)

def ecrire_lot(df, sous, nom):
    p = BASE/'normalized'/sous; p.mkdir(parents=True, exist_ok=True)
    f = p/f'{nom}.parquet'; df.to_parquet(f, index=False)
    return {'fichier': str(f.relative_to(BASE)), 'sha256': sha(f), 'lignes': int(len(df)),
            'debut': str(df.ts_utc.iloc[0]), 'fin': str(df.ts_utc.iloc[-1])}

def mode_pilot():
    mt5 = mt5_connect(); sym = os.environ.get('HFM_SYMBOL', SYMBOLE_DEFAUT)
    fin = pd.Timestamp.now(tz='UTC').floor('D'); deb = fin - pd.Timedelta(days=7)
    t = mt5.copy_ticks_range(sym, deb.to_pydatetime(), fin.to_pydatetime(), mt5.COPY_TICKS_ALL)
    if t is None or len(t)==0: raise SystemExit('PILOTE: aucun tick retourne sur 7 jours — profondeur a documenter, ne pas extrapoler.')
    df = normaliser_ticks(t, f'HFM_MT5_{sym}')
    q = qualite_ticks(df)
    man = {'mode':'pilot','symbole':sym,'specs':specs(mt5,sym),'qualite':q,
           'lot': ecrire_lot(df,'ticks',f'hfm_{sym}_ticks_pilot')}
    (BASE/'manifests'/'collection_manifest.json').write_text(json.dumps(man, indent=1, default=str))
    (BASE/'quality'/'quality_report.json').write_text(json.dumps(q, indent=1))
    print(json.dumps(man, indent=1, default=str)); mt5.shutdown()

def mode_collect(debut, fin):
    mt5 = mt5_connect(); sym = os.environ.get('HFM_SYMBOL', SYMBOLE_DEFAUT)
    man_p = BASE/'manifests'/'collection_manifest.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'lots':{}}
    for mois in pd.period_range(debut, fin, freq='M'):
        cle = str(mois)
        if man['lots'].get(cle, {}).get('statut') == 'OK': continue
        d0 = pd.Timestamp(mois.start_time, tz='UTC'); d1 = pd.Timestamp(mois.end_time, tz='UTC')
        t = mt5.copy_ticks_range(sym, d0.to_pydatetime(), d1.to_pydatetime(), mt5.COPY_TICKS_ALL)
        if t is None or len(t)==0:
            man['lots'][cle] = {'statut':'VIDE_OU_INDISPONIBLE','ticks':0}; continue
        df = normaliser_ticks(t, f'HFM_MT5_{sym}')
        lot = ecrire_lot(df, 'ticks', f'hfm_{sym}_ticks_{mois.year}_{mois.month:02d}')
        man['lots'][cle] = {'statut':'OK', **lot, 'qualite': qualite_ticks(df)}
        man_p.write_text(json.dumps(man, indent=1, default=str))
        print(cle, lot['lignes'], 'ticks')
    mt5.shutdown()

def mode_selftest():
    """Pipeline teste sur donnees SYNTHETIQUES — ne produit AUCUNE donnee HFM."""
    rng = np.random.default_rng(7)
    n = 5000; base_ms = int(pd.Timestamp('2026-01-05T08:00Z').timestamp()*1000); ms = base_ms + rng.integers(0, 300000, n).cumsum()
    mid = 4450 + np.cumsum(rng.normal(0, .05, n)); demi = rng.uniform(.08, .25, n)
    brut = pd.DataFrame({'time_msc': ms, 'bid': mid-demi, 'ask': mid+demi,
                         'last': 0.0, 'volume': 1, 'flags': 6})
    df = normaliser_ticks(brut, 'SYNTHETIC_SELFTEST_NE_JAMAIS_PUBLIER')
    q = qualite_ticks(df); assert q['bid_ge_ask']==0 and q['ts_monotones']
    lot = ecrire_lot(df, 'ticks', '_SELFTEST_SYNTHETIC')
    pathlib.Path(lot['fichier'].replace('normalized', 'normalized')).exists()
    (BASE/'quality'/'_SELFTEST_report.json').write_text(json.dumps(q, indent=1))
    print('SELFTEST OK (synthetique, fichier prefixe _SELFTEST, a exclure de toute publication):', q)
    pathlib.Path(BASE/'normalized'/'ticks'/'_SELFTEST_SYNTHETIC.parquet').unlink()


# --- Addendum seq429: adaptateurs multi-sources sans compte -----------------
# hfm_public        : aucun telechargement historique public HFM identifie (voir 4A)
# hfm_archived      : aucune archive tierce a provenance demontree identifiee (voir 4B)
# xauusd_external   : HistData (pilote CI), Dukascopy (corpus existant, non retelecharge)
# hfm_native_authenticated : modes probe/pilot/collect MT5 ci-dessus (futur, non requis)
EXT = BASE / 'external_reference'

def mode_extpilot():
    import re, zipfile, io
    import urllib.request
    EXT.mkdir(parents=True, exist_ok=True)
    res = {'source_declared': 'EXTERNAL_REFERENCE (HistData, flux generique — jamais HFM)',
           'tentatives': {}}
    # Preuve documentaire HFM Tick Chart Trader (PDF public, aucune donnee)
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            'https://static.hfm.com/assets/docs/tools_hfm/premium-trader-tools/tick-chart-trader-user-guide-HFSV-en.pdf',
            headers={'User-Agent': 'Mozilla/5.0 META-ALPHA-research'}), timeout=60)
        res['tentatives']['hfm_tickchart_pdf'] = {'http': r.status, 'octets': len(r.read(2000))}
    except Exception as e:
        res['tentatives']['hfm_tickchart_pdf'] = {'erreur': f'{type(e).__name__}: {e}'}
    # Pilote HistData XAUUSD ticks 2010-01 (formulaire public, sans compte)
    try:
        import requests
        s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 META-ALPHA-research'
        page = 'https://www.histdata.com/download-free-forex-data/?/ascii/tick-data-quotes/xauusd/2010/1'
        html = s.get(page, timeout=60).text
        tk = re.search(r'id="tk"[^>]*value="([^"]+)"', html) or re.search(r'name="tk"[^>]*value="([^"]+)"', html)
        if not tk: raise RuntimeError('jeton de formulaire HistData introuvable (page modifiee ou protection)')
        r = s.post('https://www.histdata.com/get.php', timeout=120, headers={'Referer': page},
                   data={'tk': tk.group(1), 'date': '2010', 'datemonth': '201001',
                         'platform': 'ASCII', 'timeframe': 'TICK_DATA', 'fxpair': 'XAUUSD'})
        brut = r.content
        res['tentatives']['histdata_reponse'] = {'http': r.status_code,
            'content_type': r.headers.get('Content-Type'), 'octets': len(brut),
            'debut': brut[:200].decode('ascii', 'replace')}
        if not brut[:2] == b'PK':
            import time; time.sleep(25)
            r = s.post('https://www.histdata.com/get.php', timeout=120, headers={'Referer': page},
                       data={'tk': tk.group(1), 'date': '2010', 'datemonth': '201001',
                             'platform': 'ASCII', 'timeframe': 'TICK_DATA', 'fxpair': 'XAUUSD'})
            brut = r.content
            res['tentatives']['histdata_reponse']['retry_http'] = r.status_code
            res['tentatives']['histdata_reponse']['retry_debut'] = brut[:200].decode('ascii', 'replace')
        (EXT / 'raw').mkdir(exist_ok=True)
        (EXT / 'raw' / 'HISTDATA_T_XAUUSD_201001.zip').write_bytes(brut)
        z = zipfile.ZipFile(io.BytesIO(brut)); noms = z.namelist()
        nom = [n for n in noms if n.lower().endswith('.csv')][0]
        lignes = z.read(nom).decode('ascii', 'replace').splitlines()
        res['tentatives']['histdata_201001'] = {'http': r.status_code, 'octets': len(brut),
            'fichiers_zip': noms, 'lignes_csv': len(lignes), 'premiere': lignes[0][:120],
            'derniere': lignes[-1][:120], 'sha256_zip': hashlib.sha256(brut).hexdigest()}
    except Exception as e:
        res['tentatives']['histdata_201001'] = {'erreur': f'{type(e).__name__}: {e}'}
    (EXT / 'PILOT_EXTERNAL.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv)>1 else 'selftest'
    {'probe': mode_probe, 'pilot': mode_pilot, 'selftest': mode_selftest,
     'collect': lambda: mode_collect(sys.argv[2], sys.argv[3]), 'extpilot': mode_extpilot}[m]()
