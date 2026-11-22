import math

CONTRAINTE_SOL_KPA = 200      # contrainte admissible du sol
COEF_SEMELLE = 187.5          # 200 - 12,5 (poids propre de la semelle)
CONTRAINTE_POTEAU_KPA = 10_000  # hypothèse déduite du tableau (10 MPa)
COTE_POTEAU_MIN_CM = 20


def _verifier_positif(valeur: float, nom: str) -> None:
    """Lève une ValueError si la valeur n'est pas un nombre strictement positif."""
    if not isinstance(valeur, (int, float)) or valeur <= 0:
        raise ValueError(f"{nom} doit être un nombre positif (reçu : {valeur!r})")


def _arrondi_sup(valeur: float, pas: float) -> float:
    """Arrondit une valeur au multiple supérieur du pas."""
    return round(math.ceil(round(valeur / pas, 6)) * pas, 2)


def cote_semelle(g_plus_q_kn: float) -> dict:
    """Côté B d'une semelle carrée : B >= racine((G+Q) / 187,5).

    Retourne le côté minimal (m, arrondi au cm) et le côté retenu (m, au pas de 5 cm).
    """
    _verifier_positif(g_plus_q_kn, "G+Q")
    b_min = math.sqrt(g_plus_q_kn / COEF_SEMELLE)
    return {"minimal_m": round(b_min, 2), "retenu_m": _arrondi_sup(b_min, 0.05)}


def cote_poteau(n_elu_kn: float) -> dict:
    """Section minimale et côté retenu d'un poteau carré.

    Aire = N_ELU / 10 000 (m²), côté = racine de l'aire arrondi au cm,
    côté retenu = max(côté calculé, 20 cm) au pas de 5 cm.
    """
    _verifier_positif(n_elu_kn, "N_ELU")
    aire = n_elu_kn / CONTRAINTE_POTEAU_KPA
    calcule_cm = math.ceil(round(math.sqrt(aire) * 100, 6))
    retenu_cm = int(_arrondi_sup(max(calcule_cm, COTE_POTEAU_MIN_CM), 5))
    return {"aire_m2": round(aire, 3), "calcule_cm": calcule_cm, "retenu_cm": retenu_cm}


if __name__ == "__main__":
    cas = [("Angle", 168.4, 122.1), ("Rive", 317.8, 230.1), ("Central", 616.6, 446.1)]
    for nom, n_elu, g_q in cas:
        print(nom, cote_poteau(n_elu), cote_semelle(g_q))