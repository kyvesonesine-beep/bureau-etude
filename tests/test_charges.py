"""Tests des valeurs de contrôle du prédimensionnement."""

import pytest

from src.predimensionnement import cote_poteau, cote_semelle


@pytest.mark.parametrize("n_elu, aire, calcule, retenu", [
    (168.4, 0.017, 13, 20),   # angle
    (317.8, 0.032, 18, 20),   # rive
    (616.6, 0.062, 25, 25),   # central
])
def test_poteau(n_elu, aire, calcule, retenu):
    res = cote_poteau(n_elu)
    assert res["aire_m2"] == aire
    assert res["calcule_cm"] == calcule
    assert res["retenu_cm"] == retenu


@pytest.mark.parametrize("g_q, minimal, retenu", [
    (122.1, 0.81, 0.85),   # angle
    (230.1, 1.11, 1.15),   # rive
    (446.1, 1.54, 1.55),   # central
])
def test_semelle(g_q, minimal, retenu):
    res = cote_semelle(g_q)
    assert res["minimal_m"] == minimal
    assert res["retenu_m"] == retenu


@pytest.mark.parametrize("valeur", [0, -5, "abc"])
def test_valeurs_invalides(valeur):
    with pytest.raises(ValueError):
        cote_poteau(valeur)
    with pytest.raises(ValueError):
        cote_semelle(valeur)