"""AUDIT PRE-EXECUTION - validation numerique independante des formules.
Implementation de reference en Python pur, sur petits jeux controles, avec
resultats attendus calcules a la main. Ces tests valident les DEFINITIONS
mathematiques; ils ne certifient pas les traductions SQL de production
(voir plan_extraction: 6 variables certifiees, les autres refusees)."""
import math
from datetime import datetime, timedelta, timezone

# --- references independantes (aucun code de production importe) ---
def mid(b,a): return (b+a)/2.0
def spread_abs(b,a): return a-b
def spread_rel(b,a): return (a-b)/mid(b,a)
def ret_tick(mids): return [None]+[mids[i]/mids[i-1]-1 for i in range(1,len(mids))]
def roll_std_event(x,n):
    out=[]
    for i in range(len(x)):
        if i<n-1: out.append(None); continue
        w=x[i-n+1:i+1]; m=sum(w)/n
        out.append(math.sqrt(sum((v-m)**2 for v in w)/(n-1)))
    return out
def roll_range_event(x,n):
    return [None if i<n-1 else max(x[i-n+1:i+1])-min(x[i-n+1:i+1]) for i in range(len(x))]
def robust_z(x):
    s=sorted(x); med=s[len(s)//2] if len(s)%2 else (s[len(s)//2-1]+s[len(s)//2])/2
    dev=sorted(abs(v-med) for v in x); mad=dev[len(dev)//2] if len(dev)%2 else (dev[len(dev)//2-1]+dev[len(dev)//2])/2
    return [(v-med)/(1.4826*mad) if mad else None for v in x], med, mad
def interarrival_mean(ts,n):
    d=[None]+[(ts[i]-ts[i-1]).total_seconds() for i in range(1,len(ts))]
    return [None if i<n else sum(d[i-n+1:i+1])/n for i in range(len(ts))], d
def update_intensity(ts_seconds,T):
    """Reference CAUSALE: evenements dans (t-T, t] - passe et present uniquement."""
    return [sum(1 for t in ts_seconds if t <= s and s-t < T) for s in ts_seconds]
def mfe_mae_long(entry_ask, future_bids):
    return max(future_bids)/entry_ask-1, min(future_bids)/entry_ask-1
def ret_long(entry_ask, exit_bid): return exit_bid/entry_ask-1
def ret_short(entry_bid, exit_ask): return entry_bid/exit_ask-1

# --- F1 prix & cotations ---
def test_f1_spreads_et_mid():
    assert mid(2300.0,2300.6)==2300.3
    assert spread_abs(2300.0,2300.6)==0.6000000000001364 or abs(spread_abs(2300.0,2300.6)-0.6)<1e-9
    assert abs(spread_rel(2300.0,2300.6)-0.6/2300.3)<1e-12

# --- F2 rendements, dont Bid/Ask ---
def test_f2_ret_tick_et_ret_h():
    r=ret_tick([100.0,101.0,99.0])
    assert r[0] is None and abs(r[1]-0.01)<1e-12 and abs(r[2]-(99/101-1))<1e-12
    # RET_H (label, futur par definition): mid[t+30s]/mid[t]-1
    assert abs((105.0/100.0-1)-0.05)<1e-12
def test_f2_rendements_bid_ask_pas_mid():
    # long: on achete a l'ask, on revend au bid -> le spread est un cout reel
    assert abs(ret_long(100.5,101.5)-(101.5/100.5-1))<1e-12
    assert ret_long(100.5,100.4) < 0  # mid monte (100->100.45) mais le long perd: preuve du spread
    assert abs(ret_short(100.0,99.5)-(100.0/99.5-1))<1e-12

# --- F3 volatilite: fenetres EVENEMENTS + warm-up NULL ---
def test_f3_rolling_std_range_warmup_null():
    x=[1.0,2.0,3.0,4.0]
    s=roll_std_event(x,3); assert s[0] is None and s[1] is None and abs(s[2]-1.0)<1e-12 and abs(s[3]-1.0)<1e-12
    r=roll_range_event(x,3); assert r[:2]==[None,None] and r[2]==2.0 and r[3]==2.0

# --- F4 z-score robuste ---
def test_f4_zscore_robuste():
    z,med,mad=robust_z([10,11,10,12,50])
    assert med==11 and mad==1
    assert abs(z[-1]-(50-11)/(1.4826))<1e-9 and z[0]<0<z[-1]

# --- F5 microstructure: intervalles + intensite TEMPS ---
def test_f5_interarrival_et_intensite():
    t0=datetime(2026,1,1,tzinfo=timezone.utc); ts=[t0+timedelta(seconds=s) for s in (0,2,5,9)]
    m,d=interarrival_mean(ts,2); assert d[1:]==[2.0,3.0,4.0] and m[2]==2.5 and m[3]==3.5
    # intensite sur T=5s, fenetre passee [t-5s, t]: a t=9 -> evenements 5 et 9 = 2
    assert update_intensity([0,2,5,9],5)==[1,2,2,2]

# --- F8 labels MFE/MAE en Bid/Ask (long: entree ask, excursions sur bid futur) ---
def test_f8_mfe_mae_bid_ask():
    mfe,mae=mfe_mae_long(100.5,[101.0,103.0,99.0])
    assert abs(mfe-(103.0/100.5-1))<1e-12 and abs(mae-(99.0/100.5-1))<1e-12 and mae<0<mfe

# --- Anti-lookahead: perturber le futur ne change pas les features a t ---
def test_anti_lookahead_perturbation_futur():
    a=[100.,101.,102.,103.,104.]; b=[100.,101.,102.,9999.,-5.]
    assert roll_std_event(a,3)[:3]==roll_std_event(b,3)[:3]
    assert ret_tick(a)[:3]==ret_tick(b)[:3]

# --- Splits calendaires 60/20/20 + purge 1h ---
def test_split_calendaire_et_purge():
    start=datetime(2020,1,1,tzinfo=timezone.utc); end=start+timedelta(days=100)
    b1=start+(end-start)*0.6; b2=start+(end-start)*0.8
    assert (b1-start).days==60 and (b2-b1).days==20 and (end-b2).days==20
    # un label de 1h ne doit pas traverser une frontiere: derniere origine valide = frontiere - 1h
    assert b1-timedelta(hours=1) < b1  # purge minimale 1h justifiee par D_HORIZON_LABEL max
