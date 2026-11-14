"""Generation deterministe du lot P3-002: hypotheses preenregistrees AVANT test.
105 tests de cellule (7 features x 5 quintiles x 3 horizons) + 21 contrastes Q5-Q1.
Chaque hypothese: definition, justification, protocole, criteres succes/rejet."""
import json, pathlib
feats = {
 'spread_rel':'cout de transaction relatif instantane (etat de liquidite)',
 'roll_std_100':'volatilite realisee courte (rendements mid, 100 evenements)',
 'roll_range_100':'amplitude relative des prix (100 evenements)',
 'interarrival_100':'rythme d arrivee moyen des ticks (secondes, 100 evenements)',
 'intensity_30s':'nombre de ticks sur [t-30s, t] (activite)',
 'past_ret_15m':'rendement mid passe sur 15 min (momentum/retournement)',
 'past_ret_1h':'rendement mid passe sur 1 h (momentum/retournement)'}
hors=['5m','15m','1h']
hyps=[]
for f,just in feats.items():
    for q in range(1,6):
        for h in hors:
            hyps.append({'id':f'H-{len(hyps)+1:03d}','type':'cellule','feature':f,'quintile':q,'horizon':h,
              'definition':f'moyenne de RET_H({h}) (mid-to-mid, RET_H_ALIGN_V1) pour les origines IS dont {f} est au quintile {q} (seuils globaux IS, passe A)',
              'justification':just,'protocole':'IS seul, origines %500, purge via partitions entieres, labels ASOF premier tick >= t+H',
              'succes':'|moyenne| > spread_rel median IS ET q_BH < 0.05 (filtre d ordre de grandeur economique + FDR)',
              'rejet':'sinon: conservee comme negative/non concluante, jamais retestee sur le meme echantillon'})
    for h in hors:
        hyps.append({'id':f'H-{len(hyps)+1:03d}','type':'contraste','feature':f,'quintile':'Q5-Q1','horizon':h,
          'definition':f'moyenne RET_H({h}) au quintile 5 moins quintile 1 de {f}',
          'justification':just,'protocole':'idem cellules','succes':'|ecart| > spread_rel median IS ET q_BH < 0.05','rejet':'sinon'})
out={'lot':'P3-002','n_hypotheses':len(hyps),'echantillon':'IS calendaire gele 2010-01-04 -> 2020-01-20 09:36:27','holdout':'scelle, jamais lu','hypotheses':hyps}
pathlib.Path('reports/meta_alpha/p3/P3_002_REGISTRY.json').write_text(json.dumps(out,indent=1,ensure_ascii=False))
print('hypotheses generees:', len(hyps))
