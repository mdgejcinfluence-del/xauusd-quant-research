#!/usr/bin/env python3
"""EMI-006 — Moteur causal événementiel de clôture (outil de recherche).

À chaque tick, seules les informations déjà reçues sont utilisées :
ticks passés, PWA connu, P&L latent calculable, compteurs passés.
Aucun accès au futur. Les familles P / C / H / E / U sont interchangeables
sans modifier le moteur central. Ce moteur est un outil de recherche :
il ne prétend pas reproduire le véritable EA (mécanisme non identifié,
voir EXIT_IDENTIFIABILITY_MATRIX.csv).

Entrée : CSV trajectoire colonnes ts,mid,pwa,pnl_latent_bp (Mid seulement ;
le spread, absent des trajectoires archivées, serait appliqué une seule
fois à l'exécution sur des données Bid/Ask — jamais doublé).
Décisions : WAIT, FAVOURABLE_STATE_DETECTED, CONFIRMATION_PENDING,
STATE_INVALIDATED, EXIT_AUTHORIZED, EXIT_EXECUTED, EXIT_NOT_AUTHORIZED.
"""
import pandas as pd


class ExitEngine:
    def __init__(self, family='U', theta_bp=0.0, persistence_s=None,
                 persistence_ticks=None, cadence_s=None, cadence_anchor=None,
                 require_rising_30s=False, retrace_bp=None):
        self.family = family; self.theta = theta_bp
        self.T = persistence_s; self.K = persistence_ticks
        self.N = cadence_s; self.anchor = cadence_anchor
        self.rising = require_rising_30s; self.retrace = retrace_bp

    def run(self, df):
        log = []; state = 'WAIT'; run_start = None; run_ticks = 0
        runmax = None; hist = []
        anchor = self.anchor if self.anchor is not None else df.ts.iloc[0]
        for i, row in df.iterrows():
            ts, pnl = row.ts, float(row.pnl_latent_bp); hist.append((ts, pnl))
            fav = pnl >= self.theta
            runmax = pnl if runmax is None else max(runmax, pnl)
            decision, reason = 'WAIT', 'etat non favorable'
            if fav and state in ('WAIT', 'STATE_INVALIDATED'):
                state = 'FAVOURABLE_STATE_DETECTED'; run_start = ts; run_ticks = 1
                decision, reason = state, f'pnl {pnl:.2f}bp >= theta {self.theta}bp'
            elif fav:
                run_ticks += 1
                decision, reason = 'CONFIRMATION_PENDING', 'confirmation en cours'
            if not fav and state in ('FAVOURABLE_STATE_DETECTED', 'CONFIRMATION_PENDING'):
                state = 'STATE_INVALIDATED'; run_start = None; run_ticks = 0
                decision, reason = state, 'pnl repasse sous le seuil'
            authorized = False
            if fav:
                if self.family == 'P':
                    if self.T is not None and run_start is not None and (ts - run_start).total_seconds() >= self.T:
                        authorized = True; reason = f'persistance {self.T}s atteinte'
                    if self.K is not None and run_ticks >= self.K:
                        authorized = True; reason = f'persistance {self.K} ticks atteinte'
                elif self.family == 'C':
                    if self.N and ((ts - anchor).total_seconds() % self.N) < 1e-9 or (self.N and self._on_grid(ts, anchor)):
                        authorized = True; reason = f'point de cadence {self.N}s'
                elif self.family == 'H':
                    base = self.T is None or (run_start is not None and (ts - run_start).total_seconds() >= self.T)
                    rising_ok = True
                    if self.rising:
                        past = [p for t, p in hist if t <= ts - pd.Timedelta(seconds=30)]
                        rising_ok = bool(past) and pnl > past[-1]
                    authorized = bool(base and rising_ok); reason = 'hybride: persistance + montee 30s'
                elif self.family == 'E':
                    authorized = self.retrace is not None and (runmax - pnl) >= self.retrace
                    reason = 'retracement depuis le max courant'
                elif self.family == 'U':
                    decision = 'EXIT_NOT_AUTHORIZED'
                    reason = 'famille unifiee non identifiee: aucun parametre ponctuel autorise (voir matrice EMI-006)'
            if authorized:
                log.append({'ts': ts, 'decision': 'EXIT_AUTHORIZED', 'famille': self.family,
                            'pnl_bp': pnl, 'run_ticks': run_ticks, 'motif': reason})
                log.append({'ts': ts, 'decision': 'EXIT_EXECUTED', 'famille': self.family,
                            'pnl_bp': pnl, 'run_ticks': run_ticks,
                            'motif': 'execution au tick courant (Mid; spread a appliquer une fois sur Bid/Ask)'})
                return pd.DataFrame(log)
            log.append({'ts': ts, 'decision': decision, 'famille': self.family,
                        'pnl_bp': pnl, 'run_ticks': run_ticks, 'motif': reason})
            if fav and state == 'FAVOURABLE_STATE_DETECTED':
                state = 'CONFIRMATION_PENDING'
        return pd.DataFrame(log)

    def _on_grid(self, ts, anchor):
        if not self.N:
            return False
        elapsed = (ts - anchor).total_seconds()
        return abs(elapsed / self.N - round(elapsed / self.N)) < 1e-6
