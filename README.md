# Projet 1 : Détection de Contours & Traitement d'Images

Ce projet a été réalisé dans le cadre de la formation **Ingénieur Informatique Industrielle** (Traitement d'images). Il s'agit d'une application interactive permettant d'analyser et de comparer différentes méthodes de détection de contours sur des images.

## 📋 Fonctionnalités

L'application propose une interface graphique interactive (GUI) développée avec `matplotlib` offrant les fonctions suivantes :

1.  **Chargement dynamique** : Lecture automatique des images présentes dans le dossier `images/`.
2.  **Comparaison de filtres** : Affichage simultané de 4 vues :
      * Image originale.
      * **Filtre de Sobel** (Magnitude du gradient horizontal et vertical).
      * **Filtre Laplacien** (Dérivée seconde).
      * **Détecteur de Canny** (Méthode optimale).
3.  **Interactivité** :
      * **Superposition (Overlay)** : Un bouton permet d'activer/désactiver la superposition des contours rouges sur l'image originale (avec transparence) pour mieux juger de la précision.
      * **Réglages Canny** : Deux glissières (sliders) permettent d'ajuster en temps réel les seuils d'hystérésis (Min/Max) du filtre de Canny.
4.  **Bonus Artistique 🎨** : Une fonctionnalité "Dessin au trait" (Line Art) qui utilise les contours détectés pour générer une version stylisée "croquis" de l'image.

## 🛠️ Prérequis

Assurez-vous d'avoir Python installé. Les bibliothèques suivantes sont nécessaires :

```bash
pip install opencv-python matplotlib numpy
```

## 🚀 Installation et Exécution

1.  **Structure du dossier** :
    Assurez-vous que votre projet respecte cette arborescence :

    ```text
    📁 Projet1/
    ├── 📄 Projet1.py        # Le script principal
    ├── 📁 images/           # Dossier contenant vos images de test (.jpg, .png)
    └── 📄 README.md
    ```

2.  **Ajout d'images** :
    Placez les images que vous souhaitez tester (ex: `lena_avec_bruit.jpg`, `boats.jpg`) dans le dossier `images`.

3.  **Lancement** :
    Exécutez le script via votre terminal ou IDE :

    ```bash
    python Projet1.py
    ```

## 🧪 Analyse des Opérateurs

Lors de l'utilisation, voici les comportements attendus (utiles pour la présentation orale) :

  * **Sobel** : Donne des contours assez épais. Il est robuste mais manque parfois de précision sur les détails fins.
  * **Laplacien** : Donne des contours très précis (fins), mais est **très sensible au bruit** (voir test sur `lena_avec_bruit.jpg` où il détecte tous les grains comme des bords).
  * **Canny** : Le meilleur compromis. Il filtre le bruit avant la détection et amincit les bords. Les **sliders** permettent d'éliminer les détails non pertinents en ajustant les seuils.

## 👤 Auteurs

  * **Étudiant 1** : Fiona Pontoparia
  * **Étudiant 2** : Benoit Serrain
  * **Formation** : Ingénieur Informatique Industrielle
  * **Date** : 10 Décembre 2025
