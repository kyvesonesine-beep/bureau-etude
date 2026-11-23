# bureau-etude
Cahier de charges
# Bureau d'études : prédimensionnement poteaux et semelles

Programme Python en console qui prédimensionne les poteaux et les semelles d'un bâtiment, calcule le métré, génère un devis et exporte un rapport (Projet 1, séance 6).

## Fonctionnalités

1. Saisir ou charger le projet (fichier JSON)
2. Calculer le métré
3. Descente de charges
4. Prédimensionner poteaux et semelles
5. Générer le devis
6. Exporter un rapport

## Structure du projet

```
bureau-etude/
├── README.md
├── requirements.txt
├── donnees/
│   ├── projet.json
│   └── bordereau.csv
├── src/
│   ├── elements.py
│   ├── charges.py
│   ├── predimensionnement.py
│   ├── devis.py
│   └── main.py
└── tests/
    └── test_charges.py
```

## Installation

```
pip install -r requirements.txt
```

## Lancement

Depuis la racine du projet :

```
python -m src.main
```

## Tests

```
python -m pytest
```

## Formules utilisées

- Poteau : aire = N_ELU / 10 000 (m²), côté = racine de l'aire, minimum 20 cm, arrondi à 5 cm.
- Semelle : B ≥ racine((G + Q) / 187,5), arrondi à 5 cm.
- Charges de calcul : N_ELU = 1,35 G + 1,5 Q.

## Auteur

[Nom Prénom]
