"""Les neuf moteurs ERE (Phase 4) — frontières vérifiables par les contrats.

Chaque moteur est une fonction pure sur les contrats de ere/contracts.py.
Aucun moteur ne peut attribuer un niveau de preuve au-delà de son autorité
(ere/taxonomy.py). H est derrière la porte de gouvernance ; I est séparé
en I-A (validation individuelle) et I-B (portefeuille).
"""
from __future__ import annotations

from .contracts import (
    AvisDeTestabilite, BehaviorProfile, EngineSpec, Envelope, ExperimentPlan,
    HypothesisSet, MarketWindow, ModelDossier, SignatureReport, TraderDossier,
    ValidationVerdict, content_hash,
)
from .taxonomy import EvidenceLevel, check_promotion

_oid = [0]


def _env(producer: str, level: EvidenceLevel) -> Envelope:
    _oid[0] += 1
    return Envelope(f"{producer}-{_oid[0]:04d}", producer, level)


# ---------------- A. Trader Intelligence Ingestion ----------------

def engine_a_ingest(trades: list, claims: list, missing: list, selection_process: str = "non documenté") -> TraderDossier:
    claims = [{**c, "verified": False} for c in claims]
    d = TraderDossier(_env("A", EvidenceLevel.N0_SOURCE_NON_VERIFIEE), trades, claims, missing, selection_process)
    d.validate()
    return d


# ---------------- B. Behavioral Reverse Engineering ----------------

def engine_b_profile(dossier: TraderDossier, windows: list[MarketWindow] | None = None) -> BehaviorProfile:
    trades = dossier.trades
    buys = sum(1 for t in trades if t.get("side") == "buy")
    sells = sum(1 for t in trades if t.get("side") == "sell")
    facts = [
        {"fait": "nombre_transactions", "valeur": len(trades)},
        {"fait": "achats", "valeur": buys},
        {"fait": "ventes", "valeur": sells},
    ]
    interps = []
    if buys and not sells:
        interps.append({"interpretation": "exposition unidirectionnelle acheteuse", "base": "achats>0, ventes=0"})
    if len(trades) >= 2:
        interps.append({"interpretation": "regroupement temporel possible", "base": ">=2 transactions"})
    p = BehaviorProfile(_env("B", EvidenceLevel.N2_INFERENCE), dossier.envelope.object_id, facts, interps,
                        [w.envelope.object_id for w in (windows or [])])
    p.validate()
    return p


# ---------------- C. Economic Hypothesis Engine ----------------

_FAMILIES = [
    ("recuperation_inventaire", "retour au plus haut antérieur après chute", "exige un plus haut récent comme cible"),
    ("retour_moyenne_ancre", "renforcements symétriques autour d'un ancrage", "prédit des renforcements après hausses aussi"),
    ("liquidite", "fourniture de liquidité rémunérée par le spread", "exige cotations du lieu d'exécution"),
    ("continuation_impulsion", "capture directionnelle après accélération", "prédit une persistance à horizons fixes"),
]

def engine_c_hypotheses(profile: BehaviorProfile) -> HypothesisSet:
    hyps = [{"hypothesis_id": h, "mecanisme": m, "prediction_divergente": p} for h, m, p in _FAMILIES]
    s = HypothesisSet(_env("C", EvidenceLevel.N3_HYPOTHESE), profile.envelope.object_id, hyps, includes_unknown=True)
    s.validate()
    return s


# ---------------- D. Scientific Knowledge Engine ----------------

_METHOD_CARDS = [
    {"method_id": "premier_retour", "question": "temps de retour à un niveau", "limites": "censure des trajectoires inachevées"},
    {"method_id": "distributions_conditionnelles", "question": "queues et quantiles par contexte", "limites": "dépendance temporelle des épisodes"},
    {"method_id": "identification_partielle", "question": "ensembles compatibles sans hypothèse forte", "limites": "bornes parfois larges"},
    {"method_id": "bootstrap_blocs", "question": "incertitude sur séries dépendantes", "limites": "longueur de bloc à justifier"},
]

def engine_d_knowledge(question_keywords: list[str]) -> list[dict]:
    out = [c for c in _METHOD_CARDS if any(k in c["question"] or k in c["method_id"] for k in question_keywords)]
    return out or list(_METHOD_CARDS)


# ---------------- F. Market Intelligence (catalog/index/signatures/execute) ----------------

class EngineF:
    """Découpage interne: catalog (avant E), index, signatures, execute (après E)."""

    def __init__(self, partitions: list[str]):
        self._partitions = list(partitions)

    def catalog(self) -> dict:
        return {"partitions": self._partitions, "n": len(self._partitions),
                "segments": ["découverte", "construction", "validation", "prospectif"]}

    def index_bars(self, ticks) -> list[dict]:
        """Barres causales agrégées depuis une liste de (ts_secondes, mid). Trié, sans futur."""
        bars: dict[int, list] = {}
        for ts, mid in sorted(ticks):
            bars.setdefault(int(ts) // 5 * 5, []).append(mid)
        return [{"t": t, "mid": sum(v) / len(v), "n": len(v)} for t, v in sorted(bars.items())]

    def signature_recovery(self, bars: list[dict], seuil_bp: float) -> dict:
        """Signature ME-001 simplifiée: chute >= seuil sous le plus haut 15 min -> retour complet en 24h?"""
        episodes, recovered = 0, 0
        mids = [b["mid"] for b in bars]
        for i in range(len(bars)):
            window = mids[max(0, i - 180):i + 1]
            if not window:
                continue
            hi = max(window)
            if hi > 0 and (mids[i] - hi) / hi * 10000 <= -seuil_bp:
                episodes += 1
                if any(m >= hi for m in mids[i + 1:i + 1 + 17280]):
                    recovered += 1
        return {"episodes": episodes, "recuperations": recovered,
                "taux": (recovered / episodes if episodes else None)}

    def execute(self, plan: ExperimentPlan, ticks, run_id: str = "run-001") -> SignatureReport:
        bars = self.index_bars(ticks)
        sig = self.signature_recovery(bars, plan.protocole.get("seuil_bp", 10.0))
        report = SignatureReport(
            _env("F", EvidenceLevel.N4_SIGNATURE_MESUREE), plan.envelope.object_id, run_id,
            "MEASURED" if sig["episodes"] else "NOT_EXECUTED",
            sig if sig["episodes"] else None, plan.segment_autorise,
            {"spread_bp_fourchette": [0.5, 2.0], "note": "ordre de grandeur, pas une mesure d'edge"})
        report.validate()
        return report


# ---------------- E. Experiment Design Engine ----------------

def engine_e_design(hypothesis_set: HypothesisSet, f_catalog: dict, segment: str = "découverte") -> ExperimentPlan:
    if not f_catalog.get("partitions"):
        avis = AvisDeTestabilite("NON_TESTABLE_EN_L_ETAT", "aucune partition autorisée dans le catalogue F", "partitions de marché")
    else:
        avis = AvisDeTestabilite("TESTABLE", "catalogue F non vide, expérience discriminante spécifiée")
    plan = ExperimentPlan(_env("E", EvidenceLevel.N3_HYPOTHESE),
                          [h["hypothesis_id"] for h in hypothesis_set.hypotheses],
                          {"test": "signature_recovery", "seuil_bp": 10.0, "criteres_predeclares": "taux de récupération + queue"},
                          segment, avis)
    plan.validate()
    return plan


# ---------------- G. Economic Model Identification ----------------

def engine_g_identify(hypothesis_set: HypothesisSet, reports: list[SignatureReport],
                      plan: ExperimentPlan, countersign_non_testable: bool = False) -> ModelDossier:
    refs = [("HypothesisSet", hypothesis_set.envelope.object_id, "x" * 64),
            ("ExperimentPlan", plan.envelope.object_id, "x" * 64)]
    refs += [("SignatureReport", r.envelope.object_id, "x" * 64) for r in reports]
    if plan.avis.valeur == "NON_TESTABLE_EN_L_ETAT":
        if not countersign_non_testable:
            raise ValueError("G: le NON_TESTABLE de E exige le contre-seing de G pour clore le dossier")
        qual = "NON DÉMONTRABLE AVEC LES DONNÉES DISPONIBLES"
        return ModelDossier(_env("G", EvidenceLevel.N3_HYPOTHESE), refs, qual,
                            [h["hypothesis_id"] for h in hypothesis_set.hypotheses], [], [], candidat_h=False)
    measured = [r for r in reports if r.status == "MEASURED"]
    if not measured:
        qual = "COMPATIBLE MAIS NON IDENTIFIÉ"
        lvl = EvidenceLevel.N3_HYPOTHESE
    else:
        # Discrimination non démontrée par une seule signature de fréquence:
        # plusieurs mécanismes restent compatibles -> jamais d'identification prématurée.
        qual = "COMPATIBLE MAIS NON IDENTIFIÉ"
        lvl = EvidenceLevel.N4_SIGNATURE_MESUREE
    d = ModelDossier(_env("G", lvl), refs, qual,
                     [h["hypothesis_id"] for h in hypothesis_set.hypotheses], [], [], candidat_h=False)
    d.validate()
    return d


# ---------------- H. Independent Strategy Engineering (porte) ----------------

def engine_h_gate(model_dossier: ModelDossier, approval: dict | None) -> EngineSpec:
    check_promotion("G", model_dossier.envelope.evidence_level)  # le dossier doit venir de G
    if model_dossier.envelope.evidence_level < EvidenceLevel.N5_MECANISME_ETAYE:
        raise PermissionError("Porte H fermée: mécanisme insuffisamment étayé (N5 minimum)")
    if not model_dossier.candidat_h:
        raise PermissionError("Porte H fermée: le dossier G ne déclare pas de candidature")
    spec = EngineSpec(_env("H", EvidenceLevel.N5_MECANISME_ETAYE), model_dossier.envelope.object_id,
                      "RESEARCH_ONLY", content_hash({"dossier": model_dossier.envelope.object_id}), approval)
    spec.validate()
    return spec


# ---------------- I-A. Validation individuelle ----------------

def engine_ia_validate(spec: EngineSpec, mesures: dict | None, criteres: dict, segment_independant: bool) -> ValidationVerdict:
    if not mesures:
        decision = "DONNÉES INSUFFISANTES"
        lvl = EvidenceLevel.N4_SIGNATURE_MESUREE
    elif not segment_independant:
        decision = "NON CONCLUANT"  # jamais de validation sur les données de construction
        lvl = EvidenceLevel.N4_SIGNATURE_MESUREE
    elif mesures.get("esperance_nette", 0) <= 0:
        decision = "RÉFUTÉE"
        lvl = EvidenceLevel.N4_SIGNATURE_MESUREE
    elif criteres and mesures.get("esperance_nette", 0) > 0:
        decision = "VALIDATION RÉUSSIE"
        lvl = EvidenceLevel.N7_AVANTAGE_VALIDE
        check_promotion("I-A", lvl)
    else:
        decision = "NON CONCLUANT"
        lvl = EvidenceLevel.N4_SIGNATURE_MESUREE
    v = ValidationVerdict(_env("I-A", lvl), spec.envelope.object_id, decision, mesures, criteres)
    v.validate()
    return v


# ---------------- I-B. Composition du portefeuille ----------------

def engine_ib_portfolio(verdicts: list[ValidationVerdict]) -> dict:
    admitted = [v.envelope.object_id for v in verdicts if v.decision == "VALIDATION RÉUSSIE"]
    return {"sources_admises": admitted, "n": len(admitted),
            "note": "indépendance économique à démontrer avant toute allocation; deux moteurs du même phénomène = une source"}
