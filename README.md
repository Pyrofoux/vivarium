# Vivarium

Environnement de simulation multi-agent basé sur SimplePlaygrounds.


## Dépendances
- `simple_playgrounds` v0.9.18 (*anciennement Flatland*)
- `tqdm`

## Installation

Lancer la commande
`pip install .` pour installer les dépendances



## Dynamiques de la simulation RPS
- Chaque agent a un corps physique: ils peuvent se pousser, bloquer des chemins
- Ils ont une notion d'énergie interne (de 0 à 100)

- se reproduisent en se séparant en deux (séparation d'énergie) localement: dispersion locale
- comportements bio-inspirés (braitenberg) chasse de proie, évitement de prédateur et d'obstacles

## Paramètres modifiables directement:
- Nombre d'espèces différentes
- Morphologie de chaque espèce, taille, vitesse linéaire et angulaire
- Forme de l'environnement: taille, obstacles qui séparent la carte en cases
- Espace d'observation : distance et angles de vue, entités perçues
- Comportement de chaque espèce: combinaisons de 4 comportements primitifs (Braitenberg), coefficients pour chaque comportement et chaque entité, mode de reproduction (séparation cellulaire, seuil de séparation)


# XP notes
1. vanilla
2. vanilla
3. +grid rooms 3x3
4. +grid rooms 5x5
5. + x2 linear & angular speed
6. + x2 linear & angular speed
7. vanilla
note: splitting threshold at 100 --> se séparent dès le départ, amène à une proportion ~= 20 au début, mais pas
exactement égale à cause de la première attaque sur chaque agent
