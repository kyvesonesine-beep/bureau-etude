"""Éléments porteurs (poteaux) et chargement du projet depuis un fichier JSON."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from src.predimensionnement import cote_poteau, cote_semelle

POSITIONS = ("angle", "rive", "central")


class ErreurProjet(Exception):
    """Erreur de lecture ou de validation du fichier projet."""


@dataclass
class Poteau:
    """Un poteau et la semelle qui le porte.

    n_elu_kn : charge de calcul du poteau à l'ELU (kN)
    g_plus_q_kn : charge G+Q en pied de poteau, pour la semelle (kN)
    """

    nom: str
    position: str
    n_elu_kn: float
    g_plus_q_kn: float

    def __post_init__(self) -> None:
        if self.position not in POSITIONS:
            raise ErreurProjet(
                f"Poteau {self.nom} : position '{self.position}' invalide "
                f"(attendu : {', '.join(POSITIONS)})"
            )

    def predimensionner(self) -> dict:
        """Retourne les dimensions du poteau et de sa semelle."""
        return {
            "nom": self.nom,
            "position": self.position,
            "poteau": cote_poteau(self.n_elu_kn),
            "semelle": cote_semelle(self.g_plus_q_kn),
        }


@dataclass
class Projet:
    """Un projet : un nom et une liste de poteaux."""

    nom: str
    poteaux: list = field(default_factory=list)

    def predimensionner(self) -> list:
        """Prédimensionne tous les poteaux du projet."""
        return [p.predimensionner() for p in self.poteaux]


def charger_projet(chemin: str) -> Projet:
    """Charge un projet depuis un fichier JSON.

    Lève ErreurProjet avec un message clair si le fichier est absent,
    mal formé ou incomplet.
    """
    fichier = Path(chemin)
    try:
        with fichier.open(encoding="utf-8") as f:
            donnees = json.load(f)
    except FileNotFoundError:
        raise ErreurProjet(f"Fichier introuvable : {chemin}") from None
    except json.JSONDecodeError as exc:
        raise ErreurProjet(f"JSON invalide dans {chemin} : {exc}") from None

    try:
        poteaux = [
            Poteau(p["nom"], p["position"], p["n_elu_kn"], p["g_plus_q_kn"])
            for p in donnees["poteaux"]
        ]
        return Projet(donnees["nom"], poteaux)
    except KeyError as exc:
        raise ErreurProjet(f"Champ manquant dans {chemin} : {exc}") from None