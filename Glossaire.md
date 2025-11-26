# 📚 Glossaire Technique du Projet

## 1. Les Bibliothèques (Modules)

| Bibliothèque | Alias | Description dans le projet |
| :--- | :--- | :--- |
| **OpenCV** | `cv2` | La bibliothèque principale de traitement d'images. Elle contient tous les algorithmes de vision (Sobel, Canny, lecture d'images, etc.). |
| **Matplotlib** | `plt` | Utilisée pour l'interface graphique (GUI). Elle gère l'affichage des figures, des axes et des widgets interactifs. |
| **NumPy** | `np` | Bibliothèque de calcul matriciel. Les images sont stockées sous forme de tableaux NumPy (matrices de pixels). |
| **OS** | `os` | Permet d'interagir avec le système d'exploitation (scanner le dossier pour trouver les fichiers images). |

---

## 2. Fonctions OpenCV (`cv2`)

### Lecture et Conversion
* **`cv2.imread(chemin)`** : Charge une image depuis le disque dur. Par défaut, OpenCV lit les couleurs dans l'ordre **BGR** (Bleu-Vert-Rouge).
* **`cv2.cvtColor(img, code)`** : Convertit l'espace colorimétrique d'une image.
    * `cv2.COLOR_BGR2RGB` : Pour passer du format OpenCV au format Matplotlib (affichage correct des couleurs).
    * `cv2.COLOR_BGR2GRAY` : Pour convertir l'image en niveaux de gris (nécessaire pour la détection de contours).

### Filtres et Détecteurs
* **`cv2.Sobel(src, ddepth, dx, dy)`** : Calcule le gradient (la variation d'intensité) de l'image.
    * `ddepth=cv2.CV_64F` : On utilise des nombres flottants (64 bits) pour ne pas perdre les valeurs négatives (les pentes descendantes) lors du calcul.
    * `dx=1, dy=0` : Gradient horizontal (bords verticaux).
    * `dx=0, dy=1` : Gradient vertical (bords horizontaux).
* **`cv2.magnitude(x, y)`** : Calcule la "force" totale du gradient en combinant X et Y (théorème de Pythagore : $\sqrt{x^2 + y^2}$).
* **`cv2.Laplacian(src, ddepth)`** : Calcule la dérivée seconde de l'image. Il détecte les changements brusques d'intensité mais est très sensible au bruit.
* **`cv2.Canny(image, seuil1, seuil2)`** : Le détecteur de contours optimal. Il suit plusieurs étapes (réduction de bruit, gradients, suppression des non-maxima et seuillage par hystérésis).
* **`cv2.GaussianBlur(src, ksize, sigma)`** : Applique un flou gaussien pour lisser l'image et réduire le bruit avant traitement (utilisé dans le bonus).

### Utilitaires
* **`cv2.convertScaleAbs(src)`** : Convertit les résultats mathématiques (qui peuvent être négatifs ou flottants) en entiers non signés 8 bits (0 à 255), ce qui est le format standard d'une image affichable.
* **`cv2.addWeighted(...)`** : Mélange deux images avec des poids différents. C'est la fonction clé pour la **superposition** (transparence).
* **`cv2.bitwise_not(src)`** : Inverse les couleurs de l'image (le noir devient blanc et inversement). Utilisé pour le bonus "Dessin au trait".

---

## 3. Fonctions Matplotlib (`plt`) & Interface

### Structure
* **`plt.figure(figsize=...)`** : Crée la fenêtre principale de l'application.
* **`plt.subplot(rows, cols, index)`** : Divise la fenêtre en grille pour afficher plusieurs images côte à côte.
* **`plt.subplots_adjust(...)`** : Règle les marges pour laisser de la place aux menus à gauche.

### Affichage
* **`ax.imshow(img)`** : Affiche l'image (matrice NumPy) sur un axe donné.
* **`ax.set_title("...")`** : Donne un titre à l'image.
* **`ax.axis('off')`** : Cache les graduations et les axes X/Y pour un rendu plus propre.
* **`fig.canvas.draw_idle()`** : Force le rafraîchissement de la fenêtre après une mise à jour (très important pour l'interactivité).

### Widgets (Contrôles)
* **`RadioButtons`** : Crée le menu de sélection (liste des images).
    * `.on_clicked(func)` : Définit quelle fonction lancer quand on change d'image.
* **`Button`** : Crée un bouton cliquable (pour la Superposition et le Bonus).
    * `.on_clicked(func)` : Lie le clic à une action.
* **`Slider`** : Crée une barre de défilement (glissière).
    * `.val` : Permet de lire la valeur actuelle du slider.
    * `.on_changed(func)` : Lance une mise à jour dès qu'on bouge le curseur.

---

## 4. Fonctions NumPy (`np`)

* **`np.zeros_like(img)`** : Crée une matrice (image) noire de la même taille que l'image donnée. On s'en sert pour créer le calque rouge lors de la superposition.