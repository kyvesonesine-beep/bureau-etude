"""Métré et devis estimatif des poteaux et semelles."""

import csv
from pathlib import Path

HAUTEUR_POTEAU_M = 3.0       # hauteur d'un poteau (hypothèse)
EPAISSEUR_SEMELLE_M = 0.4    # épaisseur d'une semelle (hypothèse)
RATIO_ACIER_KG_M3 = 100.0    # acier par m3 de béton (hypothèse)


class ErreurDevis(Exception):
    """Erreur de lecture du bordereau ou de calcul du devis."""


def charger_bordereau(chemin: str) -> dict:
    """Lit le bordereau CSV et retourne {designation: (unite, prix_unitaire)}."""
    fichier = Path(chemin)
    try:
        with fichier.open(encoding="utf-8-sig", newline="") as f:
            lecteur = csv.DictReader(f, delimiter=";")
            return {
                ligne["designation"]: (ligne["unite"], float(ligne["prix_unitaire"]))
                for ligne in lecteur
            }
    except FileNotFoundError:
        raise ErreurDevis(f"Bordereau introuvable : {chemin}") from None
    except (KeyError, ValueError) as exc:
        raise ErreurDevis(f"Bordereau invalide ({chemin}) : {exc}") from None


def metre(resultats: list, hauteur_m: float = HAUTEUR_POTEAU_M,
          epaisseur_m: float = EPAISSEUR_SEMELLE_M) -> dict:
    """Calcule les quantités à partir du prédimensionnement.

    resultats : liste retournée par Projet.predimensionner().
    Retourne les quantités de béton (m3), coffrage (m2) et acier (kg).
    """
    if not resultats:
        raise ErreurDevis("Aucun élément à métrer")
    beton = coffrage = 0.0
    for r in resultats:
        cote_poteau = r["poteau"]["retenu_cm"] / 100
        cote_semelle = r["semelle"]["retenu_m"]
        beton += cote_poteau ** 2 * hauteur_m + cote_semelle ** 2 * epaisseur_m
        coffrage += 4 * cote_poteau * hauteur_m
    return {
        "Béton": round(beton, 3),
        "Coffrage": round(coffrage, 2),
        "Acier": round(beton * RATIO_ACIER_KG_M3, 1),
    }


def generer_devis(quantites: dict, bordereau: dict) -> dict:
    """Multiplie chaque quantité par son prix du bordereau.

    Retourne {"lignes": [...], "total": float}.
    """
    lignes = []
    total = 0.0
    for designation, quantite in quantites.items():
        if designation not in bordereau:
            raise ErreurDevis(f"'{designation}' absent du bordereau")
        unite, prix = bordereau[designation]
        montant = round(quantite * prix, 2)
        lignes.append({"designation": designation, "quantite": quantite,
                       "unite": unite, "prix_unitaire": prix, "montant": montant})
        total += montant
    return {"lignes": lignes, "total": round(total, 2)}