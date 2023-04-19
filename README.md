# PNS-SI4-S8_Algorithmique_2

## Documents rendus 

- [Premier rendu](./rendus/premier%20rapport/Rendu-2023.31.03---Dubois%2C-El-Kateb%2C-Latapie.pdf)
- [Vidéo finale](https://clipchamp.com/watch/zba9fbpxPgG)

## Utilisation 

Requirements:
  - python3.11
  - make


### Lancement du projet

Notre IA

```bash
make ourMinmaxD2 # notre API avec notre algorithme Minmax en profondeur 2
make ourMinmaxD4 # profondeur 4
make ourMinmaxD6 # profondeur 6
```

IA enemie

```bash
make enemyOurRandom 
make enemyMedium 
make enemyAdvanced
```

Lancement de l'arène

```bash
make arena # lancement de l'arène entre notre IA et l'IA enemie
make arenalogs # lancement de l'arène entre notre IA et l'IA enemie avec logs
make arenasolver # lancement de l'arène entre notre IA et l'IA solver (https://connect4.gamesolver.org)
```

[Documentation et références](./doc/README.md)
