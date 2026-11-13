"""Protocole regimes PROPOSE (terciles 20 jours, recalcule quotidien, applique
le lendemain) - teste sur donnees controlees uniquement, NON active en production."""
def terciles(x):
    s=sorted(x); n=len(s)
    return s[n//3], s[(2*n)//3]
def classify_days(daily_vol, W=20):
    """Rendements de classe par jour: jour j classe avec les terciles des W jours precedents."""
    out=[]
    for j in range(len(daily_vol)):
        if j < W: out.append(None); continue
        lo,hi=terciles(daily_vol[j-W:j])
        v=daily_vol[j]; out.append(1 if v<=lo else 3 if v>hi else 2)
    return out
def test_warmup_20_jours_null():
    out=classify_days([float(i) for i in range(30)])
    assert out[:20]==[None]*20 and out[20] is not None
def test_application_lendemain_pas_le_jour_meme():
    vol=[10.0]*20+[0.0, 100.0]
    out=classify_days(vol)
    lo,hi=terciles(vol[:20]); assert lo==hi==10.0
    assert out[20]==1 and out[21]==3  # classes calculees avec le passe uniquement
def test_causalite_perturbation_futur():
    a=[float((i*7)%13+1) for i in range(40)]; b=a.copy(); b[35]=99999.0
    assert classify_days(a)[:35]==classify_days(b)[:35]
def test_reproductibilite():
    vol=[3.,1.,4.,1.,5.,9.,2.,6.]*6
    assert classify_days(vol)==classify_days(list(vol))
