"""Menu console du bureau d'études : prédimensionnement poteaux et semelles."""

from pathlib import Path

from src.charges import descente_charges
from src.devis import ErreurDevis, charger_bordereau, generer_devis, metre
from src.elements import ErreurProjet, charger_projet

CHEMIN_PROJET = "donnees/projet.json"
CHEMIN_BORDEREAU = "donnees/bordereau.csv"
CHEMIN_RAPPORT = "rapports/rapport.txt"

MENU = """
===== BUREAU D'ÉTUDES =====
1. Saisir / charger le projet (JSON)
2. Calculer le métré
3. Descente de charges
4. Prédimensionner poteaux et semelles
5. Générer le devis
6. Exporter un rapport
0. Quitter
"""


# ---------- Utilitaires ----------

def lire_nombre(invite: str) -> float:
    """Demande un nombre positif ou nul, et recommence tant que la saisie est invalide."""
    while True:
        saisie = input(invite).strip().replace(",", ".")
        try:
            valeur = float(saisie)
        except ValueError:
            print("  Saisie invalide : entrez un nombre.")
            continue
        if valeur < 0:
            print("  Entrez une valeur positive.")
            continue
        return valeur


def formater_montant(valeur: float) -> str:
    """Formate un montant avec des espaces entre les milliers."""
    return f"{valeur:,.0f}".replace(",", " ")


def formater_predimensionnement(resultats: list) -> str:
    """Tableau texte des dimensions retenues."""
    lignes = [f"{'Poteau':<8}{'Position':<10}{'Côté poteau':<14}{'Côté semelle':<14}"]
    for r in resultats:
        lignes.append(
            f"{r['nom']:<8}{r['position']:<10}"
            f"{str(r['poteau']['retenu_cm']) + ' cm':<14}"
            f"{str(r['semelle']['retenu_m']) + ' m':<14}"
        )
    return "\n".join(lignes)


def formater_devis(devis: dict) -> str:
    """Tableau texte du devis."""
    lignes = [f"{'Désignation':<12}{'Quantité':>10} {'Unité':<6}{'Prix unit.':>12}{'Montant':>14}"]
    for ligne in devis["lignes"]:
        lignes.append(
            f"{ligne['designation']:<12}{ligne['quantite']:>10} {ligne['unite']:<6}"
            f"{formater_montant(ligne['prix_unitaire']):>12}"
            f"{formater_montant(ligne['montant']):>14}"
        )
    lignes.append(f"{'TOTAL':<12}{'':>29}{formater_montant(devis['total']):>14}")
    return "\n".join(lignes)


# ---------- Accès à l'état du programme ----------

def obtenir_resultats(etat: dict) -> list:
    """Retourne le prédimensionnement, en le calculant si nécessaire."""
    if etat["projet"] is None:
        raise ErreurProjet("Aucun projet chargé : utilisez d'abord l'option 1.")
    if etat["resultats"] is None:
        etat["resultats"] = etat["projet"].predimensionner()
    return etat["resultats"]


def obtenir_devis(etat: dict) -> dict:
    """Retourne le devis, en le calculant si nécessaire."""
    if etat["devis"] is None:
        etat["quantites"] = metre(obtenir_resultats(etat))
        etat["devis"] = generer_devis(etat["quantites"], charger_bordereau(CHEMIN_BORDEREAU))
    return etat["devis"]


def exporter_rapport(etat: dict, chemin: str = CHEMIN_RAPPORT) -> str:
    """Écrit le rapport complet dans un fichier texte et retourne son chemin."""
    resultats = obtenir_resultats(etat)
    devis = obtenir_devis(etat)
    contenu = (
        f"RAPPORT - {etat['projet'].nom}\n\n"
        f"Prédimensionnement\n{formater_predimensionnement(resultats)}\n\n"
        f"Devis estimatif\n{formater_devis(devis)}\n"
    )
    fichier = Path(chemin)
    fichier.parent.mkdir(parents=True, exist_ok=True)
    fichier.write_text(contenu, encoding="utf-8")
    return str(fichier)


# ---------- Actions du menu ----------

def action_charger(etat: dict) -> None:
    chemin = input(f"Fichier projet [{CHEMIN_PROJET}] : ").strip() or CHEMIN_PROJET
    etat.update(projet=charger_projet(chemin), resultats=None, quantites=None, devis=None)
    print(f"Projet « {etat['projet'].nom} » chargé : {len(etat['projet'].poteaux)} poteaux.")


def action_metre(etat: dict) -> None:
    etat["quantites"] = metre(obtenir_resultats(etat))
    print("Métré :")
    for designation, quantite in etat["quantites"].items():
        print(f"  {designation} : {quantite}")


def action_descente(etat: dict) -> None:
    nb = int(lire_nombre("Nombre de niveaux : "))
    niveaux = []
    for i in range(1, nb + 1):
        print(f"Niveau {