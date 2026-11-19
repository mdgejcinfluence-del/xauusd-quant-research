"""PHASE 10 - SIMULATION STRUCTURELLE (hors budget, 0 essai, aucune hypothese de marche testee).
Regles 2-Step Pro (OWNER_CONFIG_V2): P1 +10%, P2 +4% (base reinitialisee), perte jour -4% de l'initial,
trailing -10% depuis le pic, 4 jours qualifiants >= +0,5%/phase, temps illimite (horizon de calcul 1000 j).
Processus declare: pnl journalier de base = mu + sigma_t * z, sigma_t = vol predite F3 (relative),
sigma de reference a taille 1 = 1,0%/jour. Les politiques ne font que dimensionner/filtrer ce flux.
E2: panier controle = distribution declaree a haut taux de reussite et queue gauche epaisse."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase10'; OUT.mkdir(parents=True, exist_ok=True)
f3 = pd.read_csv(R / 'phase2/f3_har/F3_DAILY_PRED.csv').dropna(subset=['pred_har'])
SIG = np.sqrt(f3.pred_har.values); SIG = SIG / np.median(SIG)
SIG_MED = 1.0
rng = np.random.default_rng(2026)
NSIM, HORIZON = 4000, 1000

def simule_phase(mu, politique, filtre_fenetres, embargo_f7, cible, rng):
    """Vecteur de trajectoires. Retourne (passe, ruine, jours_medians)."""
    n = NSIM
    eq = np.zeros(n); pic = np.zeros(n); qual = np.zeros(n, int)
    etat = np.zeros(n, int)  # 0 actif, 1 passe, -1 ruine
    jours = np.full(n, HORIZON)
    sig_pool = SIG
    for j in range(HORIZON):
        actif = etat == 0
        if not actif.any(): break
        sig_t = rng.choice(sig_pool, size=n, replace=True)
        z = rng.standard_normal(n)
        base = mu + 0.01 * sig_t * z
        # filtres (proxys declares: regime de vol predite F3 comme fenetre; decile haut = sauts F7)
        joue = np.ones(n, bool)
        if filtre_fenetres: joue &= sig_t <= 1.0
        if embargo_f7: joue &= sig_t < np.quantile(sig_pool, 0.90)
        # dimensionnement selon politique
        if politique == 'fixe':
            s = np.ones(n)
        elif politique == 'kelly_fraction':
            s = np.full(n, float(np.clip(0.5 * mu / 0.0001, 0, 2.0)))  # demi-Kelly: f = mu/sigma^2, sigma=1%
        elif politique == 'f3_asservi':
            s = np.clip(SIG_MED / np.maximum(sig_t, 0.05), 0.3, 2.5)
        elif politique == 'jeu_hardi_borne':
            dist = np.maximum(cible - eq, 0.0)          # en fractions
            sigma_vise = np.minimum(dist, 0.032)         # borne: 80% de la limite journaliere (3,2%)
            s = sigma_vise / np.maximum(0.01 * sig_t, 1e-6)
            s = np.clip(s, 0, 4.0)
        pnl = np.where(joue, base * s, 0.0)
        # apres cible atteinte mais jours qualifiants manquants: taille reduite (regle des 4 jours)
        pnl = np.where((eq >= cible) & (qual < 4), pnl * 0.1, pnl)
        eq_new = eq + pnl
        pic_new = np.maximum(pic, eq_new)
        ruine = actif & ((pnl <= -0.04) | (eq_new - pic_new <= -0.10))
        qual += (actif & (pnl >= 0.005)).astype(int)
        passe = actif & ~ruine & (eq_new >= cible) & (qual >= 4)
        jours = np.where(passe & (etat == 0), j, jours)
        etat = np.where(ruine, -1, np.where(passe, 1, etat))
        eq, pic = eq_new, pic_new
    passe = etat == 1
    return {'P': float(passe.mean()), 'P_ruine': float((etat == -1).mean()),
            'jours_medians': float(np.median(jours[passe])) if passe.any() else None,
            'P_inacheve': float((etat == 0).mean())}

E1 = {}
for mu_bp, mu in [('mu_-2bp (couts seuls)', -0.0002), ('mu_0', 0.0), ('mu_+2bp', 0.0002)]:
    for pol in ['fixe', 'kelly_fraction', 'f3_asservi', 'jeu_hardi_borne']:
        for ff, f7, lab in [(False, False, 'sans filtre'), (True, True, 'filtres M1/M5+F7')]:
            r1 = simule_phase(mu, pol, ff, f7, 0.10, rng)
            r2 = simule_phase(mu, pol, ff, f7, 0.04, rng)
            E1[f'{mu_bp}|{pol}|{lab}'] = {'P1': r1, 'P2': r2, 'P1xP2': r1['P'] * r2['P']}
            print(mu_bp, pol, lab, 'P1=', round(r1['P'], 3), 'P2=', round(r2['P'], 3), flush=True)

# E2: panier controle (distribution declaree) sous politique fixe vs chassis (meilleure E1 a mu_-2bp)
def simule_panier(rng, n=NSIM):
    eq = np.zeros(n); pic = np.zeros(n); qual = np.zeros(n, int); etat = np.zeros(n, int)
    for j in range(HORIZON):
        actif = etat == 0
        if not actif.any(): break
        u = rng.random(n)
        pnl = np.where(u < 0.92, 0.0010, np.where(u < 0.99, -0.008, -0.045))
        eq_new = eq + pnl; pic_new = np.maximum(pic, eq_new)
        ruine = actif & ((pnl <= -0.04) | (eq_new - pic_new <= -0.10))
        qual += (actif & (pnl >= 0.005)).astype(int)
        passe = actif & ~ruine & (eq_new >= 0.10) & (qual >= 4)
        etat = np.where(ruine, -1, np.where(passe, 1, etat)); eq, pic = eq_new, pic_new
    return {'P_passer_P1': float((etat == 1).mean()), 'P_ruine': float((etat == -1).mean())}
E2 = {'panier_controle_declare (92% +0,10% / 7% -0,8% / 1% -4,5% stop dur)': simule_panier(rng),
      'esperance_journaliere_panier_bp': float(0.92 * 10 - 0.07 * 80 - 0.01 * 450)}
print('E2', E2)

# E3: arithmetique du ticket (scenarios declares)
frais = {'frais_bas_$32 (repere Standard 5K)': 32, 'frais_median_$75': 75, 'frais_haut_$150': 150}
E3 = {}
meilleur = max((v['P1xP2'], k) for k, v in E1.items() if 'mu_-2bp' in k)
for lab, f in frais.items():
    for gain in [100, 200, 400]:
        E3[f'{lab} x gain_finance_${gain}'] = {'EV_a_mu_-2bp_meilleure_politique': round(meilleur[0] * gain - f, 2), 'P1xP2': round(meilleur[0], 4)}
E3['_meilleure_politique_mu_-2bp'] = meilleur[1]
E3['_regle_coherence'] = "frais engages seulement si P(echec) <= 25% (P(passage total) >= 75%) - aucune politique a mu<=0 ne l'approche"
(OUT / 'PHASE10_DATA.json').write_text(json.dumps({'E1': E1, 'E2': E2, 'E3': E3}, indent=1, default=str))

md = ['# PHASE 10 — RAPPORT DE SIMULATION STRUCTURELLE (hors budget, 0 essai)', '',
      'Processus declare: bruit journalier calibre sur la vol predite F3, esperance mu IMPOSEE (pas mesuree). Regles 2-Step exactes (V2). 4000 trajectoires/politique, horizon 1000 j.', '',
      '## E1 — P(passage) par politique (P1 x P2 entre parentheses)', '',
      '| mu impose | politique | filtres | P1 | P1xP2 | ruine P1 |', '|---|---|---|---|---|---|']
for k, v in E1.items():
    mu, pol, lab = k.split('|')
    md.append(f"| {mu} | {pol} | {lab} | {v['P1']['P']:.3f} | {v['P1xP2']:.3f} | {v['P1']['P_ruine']:.3f} |")
md += ['', '## E2 — Panier controle vs chassis', '```json', json.dumps(E2, indent=1), '```',
       '', 'Le panier affiche un taux de reussite quotidien eleve mais son esperance declaree est negative et sa queue (-4,5%) touche directement la limite journaliere: compare sa P(passage) a la meilleure ligne E1 a mu equivalent.', '',
       '## E3 — Arithmetique du ticket', '```json', json.dumps(E3, indent=1), '```', '',
       '## VERDICT E3 (une ligne)', "A esperance de marche nulle ou negative (couts), aucune politique ne porte P(passage total) pres des 75% exiges par la regle de coherence: le ticket est une loterie a prix connu, pas un achat rationnel - sauf a disposer d'une esperance directionnelle reelle, que 131 sequences n'ont pas trouvee.",
       '', '## Plafond honnete de la politique optimale',
       "La theorie des barrieres le disait (a esperance nulle, P(+a avant -b) = b/(a+b) ne depend pas du calibrage): le dimensionnement change le chemin, la duree et la queue - pas l'esperance. F3 asservi et filtres reduisent la ruine marginale; le jeu hardi borne maximise la probabilite de passage a mu donne en concentrant le risque; Kelly a mu=0 refuse de jouer (taille 0) - c'est aussi un resultat. Aucune politique ne cree le mu qui manque."]
(OUT / 'PHASE10_SIM_REPORT.md').write_text('\n'.join(md))
print('PHASE 10 SIMULATION TERMINEE')
