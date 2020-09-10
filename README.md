# vivarium


XP RPS
- réimplémentation d'un modèle de type CA
- + écologiquement valide -- qu'est-ce qu'on retrouve ? qu'est-ce qui est différent ?
- implémentation d'un premier prototype, première démo



## Dynamiques de la simulation RPS
- agent ont un corps physique -- pousser, bloquer,
- ils ont une notion d'énergie vitale (100)
 à 0 ils disparaissent, collecte chez leurs proies (+1 -1, pas de création/destruction)
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




## Requirements:
pip install `simple_playgrounds` environment from the official repo
(TODO: add link + last version)  
