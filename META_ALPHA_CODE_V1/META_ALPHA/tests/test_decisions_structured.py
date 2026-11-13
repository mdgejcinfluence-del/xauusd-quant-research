"""Reproduction : une reponse structuree du proprietaire ne doit pas lever KeyError.
Avant le correctif, _match_parameter supposait que toute valeur dict etait
l'enveloppe {answer: ...} alors que l'appelant lui passe deja la valeur."""
from metaalpha.decisions import _match_parameter

def test_structured_answer_extracts_named_parameter():
    answers = {"D_REGIME_SPREAD": {"n_classes": 3, "fenetre": "20 jours"}}
    assert _match_parameter("F5_MICROSTRUCTURE", "n_classes", answers) == 3
    assert _match_parameter("F5_MICROSTRUCTURE", "fenetre", answers) == "20 jours"

def test_structured_answer_without_named_key_returns_whole():
    answers = {"D_SEUIL_SAUT": {"principal": 4, "sensibilite": [3, 5]}}
    assert _match_parameter("F4_SAUTS_EXTREMES", "seuil", answers) == {"principal": 4, "sensibilite": [3, 5]}

def test_scalar_answer_unchanged():
    assert _match_parameter("F4_SAUTS_EXTREMES", "seuil", {"D_SEUIL_SAUT": 4}) == 4
