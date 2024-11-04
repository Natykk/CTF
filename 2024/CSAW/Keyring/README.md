# README : Défi d'Analyse par Canal Auxiliaire - Semaine 2

## Vue d'Ensemble du Défi

Cette semaine, l'objectif est d'analyser les fuites de canal auxiliaire provenant d'imprimantes 3D utilisées par KeyCorp, une entreprise spécialisée dans la fabrication de clés. Dans ce scénario, vous avez réussi à obtenir un accès physique à l'installation et avez discrètement placé un microphone et un capteur de vibration à proximité des imprimantes 3D. Votre tâche consiste à analyser les données collectées par ces capteurs pour déduire ce qui est imprimé, en les comparant avec des impressions connues.

Deux fichiers vous sont fournis pour résoudre ce défi :

- `correlation_audio.py` : Utilise la corrélation audio pour faire correspondre les signatures sonores capturées avec des signatures audio connues.
- `recherche_csv.py` : Utilise les données de vibration (coordonnées XYZ) pour analyser et faire correspondre statistiquement les échantillons avec des clés connues.

Ce README vous guidera à travers l'objectif et le fonctionnement de chaque script.

## Description des Fichiers

### 1. `correlation_audio.py`

Ce script traite les données audio de l'environnement de l'imprimante 3D pour effectuer une analyse par canal auxiliaire. Il utilise des techniques de corrélation croisée pour identifier les similarités entre les échantillons audio collectés et les signatures de clés connues.

#### Fonctionnalités Principales :

- **Conversion Audio** : Convertit les fichiers MP3 en format WAV pour l'analyse, car les calculs de corrélation sont effectués en utilisant des fichiers WAV.
- **Traitement Audio** : Lit les fichiers WAV, extrait les trames audio et les normalise pour la corrélation.
- **Calcul de Corrélation Croisée** : Calcule la corrélation croisée entre deux signaux audio pour déterminer leur similarité. Des valeurs de corrélation élevées suggèrent une correspondance entre un échantillon collecté et une signature de clé connue.
- **Visualisation** : Visualise les données de corrélation pour mettre en évidence les pics et les décalages, indicateurs d'une correspondance.

#### Utilisation

1. Placez les fichiers audio des clés connues (`KeyA.mp3`, `KeyB.mp3`, etc.) dans le répertoire `labeled/`.
2. Placez les fichiers d'échantillons capturés (`sample1.mp3`, `sample2.mp3`, etc.) dans le répertoire `unlabel/samples/`.
3. Exécutez le script. Il générera et enregistrera les résultats de corrélation croisée pour chaque paire de clé connue et d'échantillon, en affichant les correspondances les plus fortes dans `correlation.txt`.

### 2. `recherche_csv.py`

Ce script se concentre sur l'analyse des données de vibration de l'imprimante 3D. Il effectue une comparaison statistique sur les données de vibration XYZ en calculant les distances euclidiennes entre les statistiques de l'échantillon et celles des clés connues.

#### Fonctionnalités Principales :

- **Calcul Statistique** : Calcule la moyenne et l'écart type pour les coordonnées X, Y et Z des données de vibration.
- **Calcul de la Distance Euclidienne** : Mesure la distance statistique entre chaque échantillon et les clés connues. La correspondance la plus proche est identifiée comme le meilleur candidat pour la clé imprimée.
- **Sortie de Fichier** : Enregistre les statistiques calculées pour chaque échantillon dans `stats.txt` et la clé correspondante la plus proche dans `closest_key.txt`.

#### Utilisation

1. Placez les fichiers CSV contenant les données de vibration (`sample1.csv`, `sample2.csv`, etc.) dans le répertoire `samples/`.
2. Exécutez le script. Il produira les statistiques et les correspondances les plus proches dans les fichiers `stats.txt` et `closest_key.txt` respectivement.

## Prérequis

Les deux scripts nécessitent les packages Python suivants :

```bash
pip install numpy pandas scipy matplotlib pydub
``` 
