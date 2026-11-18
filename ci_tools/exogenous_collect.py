"""PACK EXOGENE - INGENIERIE DE COLLECTE UNIQUEMENT (aucune analyse, aucun test).
Double horodatage obligatoire: reference_date (decrit) / available_at_utc (connaissable).
Exposition IS: available_at_utc <= 2020-01-20T09:36:27 (fail-closed).
Sorties: reports/meta_alpha/exogenous/{MANIFEST.json, VERIFY_*.json, data_is/*.parquet} + dossiers d'upload Kaggle /tmp/pack_*.
Les perimetres scelles sont definis (choix d'ingenierie consigne): OOS = (2020-01-20, 2023-12-31], HOLDOUT > 2023-12-31."""
import io, json, hashlib, pathlib, sys, zipfile, datetime as dt
import pandas as pd, requests

OUT = pathlib.Path('reports/meta_alpha/exogenous'); OUT.mkdir(parents=True, exist_ok=True)
IS_END = pd.Timestamp('2020-01-20 09:36:27', tz='UTC')
OOS_END = pd.Timestamp('2023-12-31 23:59:59', tz='UTC')
LOG = []
def log(m): print(m, flush=True); LOG.append(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def get(url, timeout=30, essais=2):
    import time
    last=None
    for essai in range(essais):
        try:
            r = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (META ALPHA data engineering)'})
            r.raise_for_status(); return r.content
        except Exception as e:
            last=e; print(f'reessai {essai+1} {url[:60]}: {type(e).__name__}', flush=True); time.sleep(15*(essai+1))
    raise last

frames = {}   # nom -> df[reference_date, available_at_utc, colonnes valeurs]
meta = {}
def register(nom, df, source, freq, convention_dispo, famille):
    df = df.copy()
    df['reference_date'] = pd.to_datetime(df['reference_date'], utc=True)
    df['available_at_utc'] = pd.to_datetime(df['available_at_utc'], utc=True)
    frames[nom] = df.sort_values('reference_date')
    meta[nom] = {'source': source, 'frequence': freq, 'convention_available_at': convention_dispo, 'famille': famille,
                 'plage_reference': [str(df.reference_date.min()), str(df.reference_date.max())], 'lignes': int(len(df)),
                 'manquants_par_colonne': {c: int(df[c].isna().sum()) for c in df.columns}}
    log(f'OK {nom}: {len(df)} lignes {df.reference_date.min()} -> {df.reference_date.max()}')

# ---------- Famille 2+6+1(daily): FRED fredgraph ----------
FRED = {
 'DGS10': ('taux_10a', 'F2_taux_vol'), 'DGS2': ('taux_court_3m_proxy', 'F2_taux_vol'), 'DFII10': ('taux_reel', 'F2_taux_vol'),
 'VIXCLS': ('vix', 'F2_taux_vol'), 'DTWEXBGS': ('dollar_broad', 'F1_dollar'), 'DEXUSEU': ('eurusd', 'F1_dollar'),
 'DEXJPUS': ('usdjpy', 'F1_dollar'), 'SP500': ('spx', 'F6_contexte'), 'DCOILWTICO': ('wti', 'F6_contexte')}
YAHOO_FALLBACK = {'DGS10': '^TNX', 'VIXCLS': '^VIX', 'DTWEXBGS': 'DX-Y.NYB', 'DEXUSEU': 'EURUSD=X', 'DEXJPUS': 'JPY=X', 'SP500': '^GSPC', 'DCOILWTICO': 'CL=F', 'DGS2': '^IRX'}
for sid, (nom, fam) in FRED.items():
    try:
        raw = get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}')
        d = pd.read_csv(io.BytesIO(raw)); d.columns = ['reference_date', 'value']
        d = d[d.value != '.']; d['value'] = d.value.astype(float)
        d['available_at_utc'] = pd.to_datetime(d.reference_date, utc=True) + pd.Timedelta(days=1)
        register(f'fred_{nom}', d[['reference_date', 'available_at_utc', 'value']], f'FRED fredgraph id={sid}', 'daily',
                 'reference_date + 1 jour 00:00 UTC (conservateur: connaissable le lendemain)', fam)
    except Exception as e:
        log(f'ECHEC FRED {sid}: {type(e).__name__} {str(e)[:120]}')
        sym = YAHOO_FALLBACK.get(sid)
        if sym:
            try:
                raw = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=30y&interval=1d')
                j = json.loads(raw)['chart']['result'][0]; q = j['indicators']['quote'][0]
                d = pd.DataFrame({'reference_date': pd.to_datetime(j['timestamp'], unit='s', utc=True).date, 'value': q['close']})
                d = d.dropna()
                d['available_at_utc'] = pd.to_datetime(d.reference_date, utc=True) + pd.Timedelta(days=1)
                register(f'fred_{nom}', d[['reference_date', 'available_at_utc', 'value']], f'Yahoo chart {sym} (fallback FRED consigne; FRED injoignable depuis CI)', 'daily',
                         'reference_date + 1 jour 00:00 UTC (conservateur)', fam)
                continue
            except Exception as e2:
                log(f'ECHEC fallback Yahoo {sid}: {str(e2)[:100]}')
        meta[f'fred_{nom}'] = {'source': f'FRED {sid}', 'statut': 'ECHEC COLLECTE', 'motif': str(e)[:200]}

# ---------- Famille 3: volume futures Stooq -> fallback Yahoo ----------
def stooq(sym, nom, fam):
    raw = get(f'https://stooq.com/q/d/l/?s={sym}&i=d')
    d = pd.read_csv(io.BytesIO(raw))
    if 'Close' not in d.columns or len(d) < 100: raise ValueError('reponse Stooq inexploitable')
    d = d.rename(columns={'Date': 'reference_date'})
    d['available_at_utc'] = pd.to_datetime(d.reference_date, utc=True) + pd.Timedelta(hours=22)
    register(nom, d, f'Stooq {sym} daily', 'daily', 'reference_date 22:00 UTC (cloture alignee flux)', fam)
for sym, nom in [('gc.f', 'comex_gc_ohlcv'), ('si.f', 'comex_si_ohlcv')]:
    try: stooq(sym, nom, 'F3_volume')
    except Exception as e:
        log(f'ECHEC Stooq {sym}: {str(e)[:120]} — fallback Yahoo')
        try:
            raw = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym.replace(".f","=F")}?range=30y&interval=1d')
            j = json.loads(raw)['chart']['result'][0]
            q = j['indicators']['quote'][0]
            d = pd.DataFrame({'reference_date': pd.to_datetime(j['timestamp'], unit='s', utc=True).date,
                              'Open': q['open'], 'High': q['high'], 'Low': q['low'], 'Close': q['close'], 'Volume': q['volume']})
            d['available_at_utc'] = pd.to_datetime(d.reference_date, utc=True) + pd.Timedelta(hours=22)
            register(nom, d, f'Yahoo chart {sym} (fallback consigne)', 'daily', 'reference_date 22:00 UTC', 'F3_volume')
        except Exception as e2:
            log(f'ECHEC fallback Yahoo {sym}: {str(e2)[:120]}'); meta[nom] = {'source': sym, 'statut': 'ECHEC COLLECTE (2 sources)', 'motif': str(e2)[:200]}

# ---------- Famille 5: CFTC COT disaggregated (or COMEX) ----------
cot_frames = []
for year in range(2010, dt.date.today().year + 1):
    try:
        raw = get(f'https://www.cftc.gov/files/dea/history/fut_disagg_txt_{year}.zip', timeout=120)
        z = zipfile.ZipFile(io.BytesIO(raw))
        name = [n for n in z.namelist() if n.endswith('.txt')][0]
        d = pd.read_csv(io.BytesIO(z.read(name)), low_memory=False)
        colmap = {c.lower(): c for c in d.columns}
        mcol = [c for c in d.columns if 'market_and_exchange' in c.lower()][0]
        g = d[d[mcol].astype(str).str.contains('GOLD - COMMODITY EXCHANGE', na=False)]
        if len(g) == 0: log(f'COT {year}: aucune ligne GOLD'); continue
        datecol = [c for c in d.columns if c.lower().startswith('report_date')][0]
        keep = [datecol] + [c for c in d.columns if any(k in c.lower() for k in ['open_interest_all', 'm_money_positions_long', 'm_money_positions_short', 'prod_merc_positions_long', 'prod_merc_positions_short'])]
        g = g[keep].copy(); g.columns = ['reference_date'] + [c.lower()[:40] for c in keep[1:]]
        cot_frames.append(g); log(f'COT {year}: {len(g)} semaines or')
    except Exception as e:
        log(f'ECHEC COT {year}: {type(e).__name__} {str(e)[:100]}')
if cot_frames:
    cot = pd.concat(cot_frames).drop_duplicates('reference_date')
    # reference = mardi; publication vendredi 20:30 UTC (conservateur, apres 15:30 ET)
    ref = pd.to_datetime(cot.reference_date, utc=True)
    cot['available_at_utc'] = ref + pd.to_timedelta((4 - ref.dt.weekday) % 7, unit='D') + pd.Timedelta(hours=20, minutes=30)
    register('cftc_cot_gold_disagg', cot, 'CFTC fut_disagg_txt annuel (cftc.gov)', 'weekly',
             'positions du mardi, publiees vendredi 20:30 UTC (conservateur)', 'F5_positionnement')
else:
    meta['cftc_cot_gold_disagg'] = {'source': 'CFTC', 'statut': 'ECHEC COLLECTE'}

# ---------- Famille 4: macro point-in-time — NON COLLECTEE (fail-closed, motif consigne) ----------
meta['macro_calendrier_pit'] = {'source': 'ALFRED vintage (fred.stlouisfed.org)',
    'statut': 'NON COLLECTE — aucune exposition',
    'motif': 'les dates de vintage ALFRED exigent une cle API FRED (gratuite mais personnelle, absente des secrets CI); toute approximation de available_at violerait la regle anti-revision du §3. Champs laisses vides, aucune imputation. A collecter des que le proprietaire fournit une cle API FRED en secret CI.'}
meta['etf_gld_iau_shares'] = {'source': 'Yahoo shares outstanding GLD/IAU', 'statut': 'NON COLLECTE',
    'motif': 'historique lacunaire non certifiable gratuitement; consigne conformement a l instruction (famille 5, limite connue).'}

# ---------- Decoupage par perimetre + audit anti-fuite + ecriture ----------
def perimetre(df):
    a = df.available_at_utc
    return df[a <= IS_END], df[(a > IS_END) & (a <= OOS_END)], df[a > OOS_END]
packs = {'is': {}, 'oos': {}, 'holdout': {}}
for nom, df in frames.items():
    i, o, h = perimetre(df)
    for pk, part in [('is', i), ('oos', o), ('holdout', h)]:
        if len(part): packs[pk][nom] = part
for pk in packs:
    d = OUT / f'data_{pk}' if pk == 'is' else pathlib.Path(f'/tmp/pack_{pk}')
    d.mkdir(parents=True, exist_ok=True)
    for nom, part in packs[pk].items():
        part.to_parquet(d / f'{nom}.parquet', index=False)
verify = {}
for pk in ['is', 'oos', 'holdout']:
    d = OUT / f'data_{pk}' if pk == 'is' else pathlib.Path(f'/tmp/pack_{pk}')
    files = {}
    for f in sorted(d.glob('*.parquet')):
        files[f.name] = {'sha256': sha(f.read_bytes()), 'taille': f.stat().st_size}
    audit = None
    if pk == 'is':
        mx = max(pd.read_parquet(OUT / 'data_is' / fn).available_at_utc.max() for fn in files) if files else None
        audit = {'max_available_at_utc_expose': str(mx), 'borne': str(IS_END), 'passe': bool(mx is not None and mx <= IS_END)}
    verify[pk] = {'fichiers': files, 'audit_anti_fuite': audit, 'statut': 'EXPOSE' if pk == 'is' else 'SCELLE (upload seul, aucun telechargement par un moteur)'}
    (OUT / f'VERIFY_{pk.upper()}.json').write_text(json.dumps(verify[pk], indent=1, default=str))
manifest = {'mission': 'EXOGENOUS_PACK (ingenierie seule, 0 essai)', 'genere_utc': str(pd.Timestamp.now(tz='UTC')),
            'bornes': {'IS_expose': f'available_at_utc <= {IS_END}', 'OOS_scelle': f'({IS_END}, {OOS_END}]', 'HOLDOUT_scelle': f'> {OOS_END}',
                       'note': 'decoupage OOS/HOLDOUT = choix d ingenierie consigne, aucune analyse ne l a motive'},
            'regle_jointure_future': 'toute jointure avec le corpus tick utilisera available_at_utc, jamais reference_date',
            'series': meta, 'journal_collecte': LOG}
(OUT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=1, default=str))
log('COLLECTE TERMINEE')
EOF_MARKER_NOT_USED = True
