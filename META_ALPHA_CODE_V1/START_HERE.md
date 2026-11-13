# META ALPHA — PAR ICI

Deux éléments. Lis les deux, dans cet ordre.

| Fichier | Quoi |
|---|---|
| **`PASSATION_AGENT_SUCCESSOR_V1.md`** | 990 lignes. Objectif, rigueur, architecture, ton rôle, ce qui existe, ce qui reste, les erreurs déjà commises. **Lis-le en entier avant d'écrire du code.** |
| **`META_ALPHA_CODE_V1.zip`** | 73 fichiers, 8 330 lignes de Python, 143 tests verts. Vérifié par décompression dans un répertoire vierge. |

---

## Vérification en 60 secondes

```bash
unzip META_ALPHA_CODE_V1.zip && cd META_ALPHA
pip install -r requirements.txt
python -m pytest tests/ -q          # attendu : 143 passed
```

Si ce n'est pas 143, arrête-toi et rapporte. Ne « répare » rien à l'aveugle.

## Ton premier travail, dans l'ordre

1. Lis `docs/PASSATION_AGENT_SUCCESSOR_V1.md` intégralement.
2. Lis `/home/user/uploads/META_ALPHA_MISSION_SCIENTIFIQUE_BLUE_GUARDIAN_AGENT_V2.md` (717 lignes) — le propriétaire l'a fourni.
3. Crée le dépôt GitHub **public**, installe le hook (`python scripts/install_hooks.py`), pousse.
4. Configure l'accès Drive : compte de service + partage du dossier en **Lecteur** + secrets GitHub.
5. **`python -m metaalpha.drive_preflight`** ← le moment de vérité. `PASS` avec 348 partitions, ou rapport d'écart au propriétaire. **Ne force rien.**
6. Découvre le schéma réel : `build_inventory`. Documente-le.
7. Fais monter l'échelle : `advance`. Le système va jusqu'à L4 seul, puis s'arrête et réclame 9 décisions.
8. Présente les 9 décisions au propriétaire. **Ne réponds jamais à sa place.**
9. Termine la phase 2 analytique, puis demande son acceptation. **Attends.**
10. Écris ensuite les moteurs P3→P7 contre le schéma réel (§9 de la passation).

## Les cinq choses à ne pas rater

- **Le dépôt est public par décision du propriétaire.** Trois barrières empêchent les secrets d'y entrer. Ne les désactive pas.
- **Aucun GPU.** La CI casse le build si tu en introduis un.
- **`NO_EDGE` est un résultat valide.** Ne fabrique jamais un portefeuille pour satisfaire une cible.
- **Ne franchis jamais un gate seul.** Tu t'arrêtes et tu attends l'acceptation.
- **Ne pose pas une question dont la réponse est dans un document.** Le propriétaire l'a explicitement reproché.

## Le contexte humain

Le propriétaire n'est pas développeur. Il veut un système qui travaille sans lui. Il accepte `NO_EDGE`. Il a assumé le risque du dépôt public avec son conseil. Il a corrigé une chose importante : les familles de variables ne sont pas à lui de les définir — elles sont dans le dossier de spécification, et le système les instancie lui-même.

Et surtout, §14 de la passation : **ne lui dis jamais qu'un résultat est prometteur avant qu'il ne soit qualifié.**

---

*Ce fichier est un raccourci. La passation complète fait autorité.*
