"""Descente de charges : cumul des charges G et Q sur un poteau."""

COEF_G = 1.35  # coefficient ELU sur les charges permanentes
COEF_Q = 1.5   # coefficient ELU sur les charges d'exploitation


def _verifier_positif(valeur: float, nom: str) -> None:
    """Lève une ValueError si la valeur n'est pas un nombre positif ou nul."""
    if not isinstance(valeur, (int, float)) or valeur < 0:
        raise ValueError(f"{nom} doit être un nombre positif (reçu : {valeur!r})")


def combinaisons(g_kn: float, q_kn: float) -> dict:
    """Calcule les charges de calcul à partir de G et Q (kN).

    - n_elu_kn    = 1,35 G + 1,5 Q  (dimensionnement du poteau)
    - g_plus_q_kn = G + Q           (dimensionnement de la semelle)
    """
    _verifier_positif(g_kn, "G")
    _verifier_positif(q_kn, "Q")
    return {
        "g_kn": round(g_kn, 1),
        "q_kn": round(q_kn, 1),
        "n_elu_kn": round(COEF_G * g_kn + COEF_Q * q_kn, 1),
        "g_plus_q_kn": round(g_kn + q_kn, 1),
    }


def charge_niveau(surface_m2: float, g_kn_m2: float, q_kn_m2: float) -> tuple:
    """Charges (G, Q) en kN apportées par un niveau sur un poteau.

    surface_m2 : surface d'influence du poteau à ce niveau
    g_kn_m2, q_kn_m2 : charges permanentes et d'exploitation par m²
    """
    _verifier_positif(surface_m2, "surface")
    _verifier_positif(g_kn_m2, "g")
    _verifier_positif(q_kn_m2, "q")
    return surface_m2 * g_kn_m2, surface_m2 * q_kn_m2


def descente_charges(niveaux: list) -> dict:
    """Cumule les charges de tous les niveaux au-dessus d'un poteau.

    niveaux : liste de tuples (surface_m2, g_kn_m2, q_kn_m2), un par niveau.
    """
    if not niveaux:
        raise ValueError("Au moins un niveau est nécessaire")
    g_total = q_total = 0.0
    for surface, g, q in niveaux:
        g_niveau, q_niveau = charge_niveau(surface, g, q)
        g_total += g_niveau
        q_total += q_niveau
    return combinaisons(g_total, q_total)