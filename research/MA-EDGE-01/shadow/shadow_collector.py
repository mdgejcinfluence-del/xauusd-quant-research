#!/usr/bin/env python3
"""Collecte SHADOW (aucun ordre). Lit un flux de cotations fourni par l'utilisateur
(fichier CSV horodaté: timestamp_utc,bid,ask) et journalise les cotations brutes.
Refuse les horodatages anterieurs a la borne du holdout consomme."""
import csv, pathlib, sys
BORNE = '2026-09-30T23:59:58.864'
def main(src, dst):
    n = 0
    with open(src) as f, open(dst, 'a', newline='') as g:
        r, w = csv.DictReader(f), csv.writer(g)
        for row in r:
            if row['timestamp_utc'] <= BORNE: continue
            w.writerow([row['timestamp_utc'], row['bid'], row['ask']]); n += 1
    print(f'{n} cotations post-borne journalisees dans {dst}')
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
