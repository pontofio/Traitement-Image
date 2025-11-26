# 📷 Projet 1 : Détection de Contours & Traitement d'Images

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-GUI-orange?style=flat-square)

Ce projet a été réalisé dans le cadre de la formation **Ingénieur Informatique Industrielle** (Module : Traitement d'images). Il s'agit d'une application interactive permettant d'analyser, de comparer et de visualiser en temps réel différentes méthodes de détection de contours.

## 📋 Fonctionnalités

L'application propose une interface graphique interactive (GUI) développée avec `matplotlib` offrant les fonctions suivantes :

### 1. Visualisation Multi-Vues
L'écran est divisé en 4 zones pour une comparaison immédiate :
* **Image Originale** : L'image source en couleur.
* **Filtre de Sobel** : Calcul de la magnitude du gradient (combinaison des dérivées horizontale et verticale).
* **Filtre Laplacien** : Calcul de la dérivée seconde (détection de changements brusques).
* **Détecteur de Canny** : Méthode optimale avec réduction de bruit et hystérésis.

### 2. Interactivité Avancée
* **Chargement Dynamique** : Scan automatique du dossier `images/` (limité aux 20 premiers fichiers pour la fluidité).
* **Superposition (Overlay)** : Un bouton permet d'activer/désactiver la superposition des contours (en rouge) sur l'image originale. Cela permet de juger précisément la localisation des bords détectés.
* **Réglages Canny en Temps Réel** : Deux *sliders* permettent d'ajuster dynamiquement les seuils min et max de l'hystérésis du filtre de Canny.

### 3. Bonus Artistique 🎨
Le bouton **"Bonus : Dessin"** ouvre une fenêtre indépendante générant un effet "Line Art" (croquis). L'algorithme inverse le résultat du filtre de Canny pour produire des traits noirs sur fond blanc.

---

## 🛠️ Prérequis et Installation

### Dépendances
Assurez-vous d'avoir Python installé. Les bibliothèques suivantes sont nécessaires :

```bash
pip install opencv-python matplotlib numpy
````

### Structure du Dossier

Voici l'arborescence complète du projet incluant les livrables :

```text
📁 Projet1/
├── 📄 Projet1.py          # Le script principal (Application)
├── 📄 Glossaire.md        # Documentation technique des fonctions
├── 📄 README.md           # Ce fichier de présentation
├── 📄 projet 1.pdf        # Énoncé du projet / Rapport technique
├── 📄 Presentation.pptx   # Support de présentation orale (Slides)
└── 📁 images/             # Dossier contenant les images à traiter
    ├── boats.jpg
    ├── clown.jpg
    ├── lena_avec_bruit.jpg
    └── ...
```

> **Note** : Le script charge automatiquement les fichiers `.jpg`, `.jpeg` et `.png` présents dans le dossier `images/`.

-----

## 🚀 Utilisation

1.  **Préparation** : Placez vos images dans le dossier `images`.
2.  **Lancement** : Exécutez le script via votre terminal :
    ```bash
    python Projet1.py
    ```
3.  **Navigation** :
      * Sélectionnez une image dans le menu de gauche.
      * Utilisez les **glissières (sliders)** pour affiner la détection de Canny.
      * Cliquez sur **Superposition** pour voir les contours en rouge sur l'image.

-----

## 🧪 Analyse Technique des Opérateurs

Voici les spécificités techniques implémentées dans ce projet (détails complets dans `Glossaire.md`) :

| Filtre | Description Technique | Observation |
| :--- | :--- | :--- |
| **Sobel** | Utilisation de `CV_64F` pour conserver les gradients négatifs avant de calculer la magnitude $\sqrt{dx^2 + dy^2}$. | Contours épais, robuste mais manque de finesse sur les détails. |
| **Laplacien** | Calcul de la dérivée seconde (Laplacien). | Contours très fins mais extrêmement **sensible au bruit** (détecte le grain de l'image comme un bord). |
| **Canny** | Algorithme multi-étapes (Gaussien + Sobel + Non-max suppression + Hystérésis). | Le meilleur compromis. Les seuils réglables permettent d'isoler les contours structurels en ignorant le bruit. |

-----

## 👤 Auteurs

  * **Fiona Pontoparia** 
  * **Benoit Serrain** 
  * **Formation** : FA27 INFO
  * **Date** : 10 Décembre 2025

<!-- end list -->

```
```
