"""
-------------------------------------------------------------------------------
PROJET 1 : DÉTECTION DE CONTOURS
-------------------------------------------------------------------------------
Auteur      : FIona Pontoparia & Benoit Serrain
Formation   : Ingénieur Informatique Industrielle
Date        : Décembre 2025
Description : 
    Application interactive permettant de :
    1. Charger des images depuis un dossier local.
    2. Appliquer et comparer 3 filtres de détection de contours :
       - Sobel (Gradient horizontal + vertical)
       - Laplacien (Dérivée seconde)
       - Canny (Détecteur optimal avec seuils réglables)
    3. Superposer les contours sur l'image originale (Transparence).
    4. Bonus : Générer un rendu "Dessin au trait" artistique.

Dépendances : opencv-python, matplotlib, numpy
-------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, Slider
import cv2
import os
import numpy as np
import random

# =============================================================================
# 1. CONFIGURATION & INITIALISATION
# =============================================================================

dossier_img = 'images'

# Vérification de l'existence du dossier
if not os.path.exists(dossier_img):
    os.makedirs(dossier_img)
    print(f"[INFO] Dossier '{dossier_img}' créé. Veuillez y ajouter vos images.")
    exit()

# Récupération des fichiers images (filtre par extension)
fichiers = [f for f in os.listdir(dossier_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not fichiers:
    print(f"[ERREUR] Aucune image trouvée dans le dossier '{dossier_img}'.")
    exit()

# On limite la liste à 20 images pour ne pas surcharger l'interface
if len(fichiers) > 20:
    fichiers = fichiers[:20]


# =============================================================================
# 2. MISE EN PAGE DE L'INTERFACE (MATPLOTLIB)
# =============================================================================

# Création de la fenêtre principale
fig = plt.figure(figsize=(16, 9))
fig.canvas.manager.set_window_title('Projet 1 : Détection de Contours - Interactif')

# --- Définition des zones (Rectangles [left, bottom, width, height]) ---
rect_menu       = [0.02, 0.55, 0.20, 0.40]   # Menu de sélection des images (Haut Gauche)
rect_btn        = [0.05, 0.48, 0.15, 0.05]   # Bouton ON/OFF Superposition
rect_slider1    = [0.05, 0.40, 0.15, 0.03]   # Slider Seuil Min (Canny)
rect_slider2    = [0.05, 0.35, 0.15, 0.03]   # Slider Seuil Max (Canny)
rect_bonus      = [0.05, 0.25, 0.15, 0.06]   # Bouton Bonus Artistique
rect_bonus_woaw = [0.05, 0.15, 0.15, 0.06]   # Bouton Bonus Artistique WOAW

# Ajustement de la zone d'affichage des images (Laisser de la place à gauche pour le menu)
plt.subplots_adjust(left=0.30, right=0.98, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)

# --- Création des sous-figures (Subplots) ---
ax_original = plt.subplot(2, 2, 1)  # Image originale (Haut Gauche)
ax_sobel    = plt.subplot(2, 2, 2)  # Résultat Sobel (Haut Droite)
ax_lap      = plt.subplot(2, 2, 3)  # Résultat Laplacien (Bas Gauche)
ax_canny    = plt.subplot(2, 2, 4)  # Résultat Canny (Bas Droite)


# =============================================================================
# 3. CRÉATION DES WIDGETS
# =============================================================================

# Ajout d'un fond gris esthétique pour le panneau de contrôle
fig.patches.extend([plt.Rectangle((0, 0), 0.28, 1, fill=True, color='#f0f0f0', alpha=1, zorder=-1, transform=fig.transFigure)])
fig.text(0.02, 0.96, "PANNEAU DE CONTRÔLE", fontsize=12, fontweight='bold', color='#333')

# A. Menu Radio (Liste des images)
ax_radio = plt.axes(rect_menu, facecolor='#e8e8e8')
radio = RadioButtons(ax_radio, fichiers, active=0)

# B. Bouton Superposition
ax_btn = plt.axes(rect_btn)
btn_superpo = Button(ax_btn, 'Superposition : ON', color='lightblue', hovercolor='0.975')

# C. Sliders pour Canny (Permet d'ajuster l'hystérésis en temps réel)
ax_slide1 = plt.axes(rect_slider1)
ax_slide2 = plt.axes(rect_slider2)
s_canny_min = Slider(ax_slide1, 'Seuil Min', 0, 255, valinit=100, color='gray')
s_canny_max = Slider(ax_slide2, 'Seuil Max', 0, 255, valinit=200, color='gray')

# D. Bouton Bonus
ax_btn_bonus = plt.axes(rect_bonus)
btn_bonus = Button(ax_btn_bonus, '✏️ Bonus : Dessin', color='#ffebcd', hovercolor='#ffd700')
ax_btn_bonus_woaw = plt.axes(rect_bonus_woaw)
btn_bonus_woaw = Button(ax_btn_bonus_woaw, '✏️ Bonus : Dessin WOAW', color="#cab99e", hovercolor='#ffd700')

# Variable globale pour suivre l'état du bouton (Vrai = Superposition activée)
etat_superposition = True 


# =============================================================================
# 4. FONCTIONS DE TRAITEMENT D'IMAGE
# =============================================================================

def superposer_contours(image_rgb, masque_gris):
    """
    Superpose un masque de contours (converti en rouge) sur l'image originale.
    
    Args:
        image_rgb: L'image couleur originale.
        masque_gris: L'image des contours (niveaux de gris 0-255).
        
    Returns:
        Une image fusionnée.
    """
    # 1. On crée une image noire de la même taille
    contours_couleur = np.zeros_like(image_rgb)
    # 2. On affecte le masque uniquement au canal ROUGE (canal 0 dans Matplotlib/RGB)
    contours_couleur[:, :, 0] = masque_gris 
    
    # 3. Fusion pondérée (Alpha Blending) : 
    # 100% de l'image originale + 80% des contours rouges + gamma 0
    return cv2.addWeighted(image_rgb, 1.0, contours_couleur, 0.8, 0)

def colorier_zones(dessin_noir_blanc):
    """
    dessin_noir_blanc : image avec fond blanc et traits noirs (0/255)
    Retourne une image RGB colorée, chaque zone ayant une couleur différente.
    """

    # 1) Les traits noirs = murs (0), le reste = zones (1)
    #    On convertit en masque binaire exploitable
    masque = (dessin_noir_blanc == 255).astype(np.uint8)

    # 2) Détection des zones connectées
    nb_composantes, labels = cv2.connectedComponents(masque, connectivity=4)

    # 3) Création de couleurs aléatoires
    couleurs = {
        i: np.array([
            random.randint(40, 255),
            random.randint(40, 255),
            random.randint(40, 255)
        ], dtype=np.uint8)
        for i in range(1, nb_composantes)  # 0 = fond blanc
    }

    # 4) Construction de l’image colorée
    h, w = labels.shape
    image_color = np.full((h, w, 3), 255, np.uint8)  # fond blanc

    for y in range(h):
        for x in range(w):
            label = labels[y, x]
            if label != 0:  # 0 = fond
                image_color[y, x] = couleurs[label]

    return image_color

def creer_dessin_trait(img_rgb, seuil1, seuil2):
    """
    BONUS : Génère un effet "Dessin au trait" (Line Art).
    
    Args:
        img_rgb: Image source.
        seuil1, seuil2: Paramètres d'hystérésis pour Canny.
    
    Returns:
        Une image RGB représentant le dessin (traits noirs sur fond blanc).
    """
    # Conversion en niveaux de gris
    gris = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    # 1. Flou Gaussien : Lisse l'image pour éviter de dessiner le "bruit" (les petits détails)
    gris_flou = cv2.GaussianBlur(gris, (3, 3), 0)
    
    # 2. Détection de Canny : Trouve les bords (pixels blancs sur fond noir)
    bords = cv2.Canny(gris_flou, seuil1, seuil2)
    
    # 3. Inversion des couleurs (Bitwise NOT) :
    # On veut des traits NOIRS sur fond BLANC (comme un dessin papier).
    dessin = cv2.bitwise_not(bords)
    
    # 4. Conversion en RGB pour affichage correct via Matplotlib
    dessin_rgb = cv2.cvtColor(dessin, cv2.COLOR_GRAY2RGB)
    
    return dessin_rgb

def creer_dessin_trait_woaw(img_rgb, seuil1=100, seuil2=127):
    """Combine dessin au trait + remplissage couleurs uniques."""
    
    # 1) Canny
    gris = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    #flou = cv2.GaussianBlur(gris, (3, 3), 0)
    edges = cv2.Canny(flou, seuil1, seuil2)

    # 2) Inverser (traits noirs, fond blanc)
    dessin = cv2.bitwise_not(edges)

    # 3) Colorisation zone par zone
    color = colorier_zones(dessin)

    # 4) Replacer les traits noirs au-dessus
    traits_noirs = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    traits_noirs = cv2.threshold(traits_noirs, 1, 255, cv2.THRESH_BINARY_INV)[1]

    # On applique les traits par AND logique
    final = cv2.bitwise_and(color, traits_noirs)

    return final


# =============================================================================
# 5. GESTION DES ÉVÉNEMENTS (CALLBACKS)
# =============================================================================

def basculer_superposition(event):
    """Active ou désactive l'affichage des contours par-dessus l'image."""
    global etat_superposition
    etat_superposition = not etat_superposition
    
    # Mise à jour visuelle du bouton
    if etat_superposition:
        btn_superpo.label.set_text('Superposition : ON')
        btn_superpo.color = 'lightblue'
    else:
        btn_superpo.label.set_text('Superposition : OFF')
        btn_superpo.color = 'white'
    
    # On relance le calcul et l'affichage
    update()


def ouvrir_fenetre_bonus(event):
    """
    Ouvre une NOUVELLE fenêtre Matplotlib indépendante pour afficher le bonus.
    Cela permet de ne pas écraser l'interface principale.
    """
    # Récupération de l'image active
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    # Conversion BGR -> RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # On utilise les valeurs actuelles des sliders pour que le dessin corresponde
    # aux réglages que l'utilisateur vient de tester.
    s1 = s_canny_min.val
    s2 = s_canny_max.val
    
    # Calcul de l'effet artistique
    img_art = creer_dessin_trait(img_rgb, s1, s2)
    
    # Création de la fenêtre Popup
    fig_bonus = plt.figure(figsize=(8, 8))
    fig_bonus.canvas.manager.set_window_title(f'BONUS - Dessin au trait : {nom_image}')
    
    plt.imshow(img_art)
    plt.title(f"Effet 'Line Art' (Canny Inversé)\nSeuils utilisés: {int(s1)} / {int(s2)}", fontsize=14)
    plt.axis('off')
    plt.show()


def ouvrir_fenetre_bonus_woaw(event):
    """
    Ouvre une NOUVELLE fenêtre Matplotlib indépendante pour afficher le bonus.
    Cela permet de ne pas écraser l'interface principale.
    """
    # Récupération de l'image active
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    # Conversion BGR -> RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # On utilise les valeurs actuelles des sliders pour que le dessin corresponde
    # aux réglages que l'utilisateur vient de tester.
    s1 = s_canny_min.val
    s2 = s_canny_max.val
    
    # Calcul de l'effet artistique
    img_art = creer_dessin_trait_woaw(img_rgb, s1, s2)
    
    # Création de la fenêtre Popup
    fig_bonus = plt.figure(figsize=(8, 8))
    fig_bonus.canvas.manager.set_window_title(f'BONUS - Dessin au trait : {nom_image}')
    
    plt.imshow(img_art)
    plt.title(f"Effet 'Line Art' (Canny Inversé)\nSeuils utilisés: {int(s1)} / {int(s2)}", fontsize=14)
    plt.axis('off')
    plt.show()


def update(val=None):
    """
    Fonction principale : lit l'image, calcule les filtres et met à jour l'affichage.
    Appelée à chaque changement (clic image, slider, bouton).
    """
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    
    # Lecture avec OpenCV (charge en BGR par défaut)
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    # Conversions nécessaires
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)   # Pour affichage couleur correct
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY) # Pour le calcul des gradients
    
    # ---------------------------------------------------------
    # 1. FILTRE DE SOBEL
    # ---------------------------------------------------------
    # Calcul des dérivées horizontales (dx=1, dy=0) et verticales (dx=0, dy=1).
    # Utilisation de CV_64F (flottants) pour éviter de perdre les valeurs négatives
    # lors du calcul de la dérivée (passage du blanc au noir).
    gx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Magnitude du gradient : racine(gx^2 + gy^2)
    magnitude = cv2.magnitude(gx, gy)
    # Reconversion en entiers 8 bits (0-255) pour l'affichage
    sobel = cv2.convertScaleAbs(magnitude)

    # ---------------------------------------------------------
    # 2. FILTRE LAPLACIEN
    # ---------------------------------------------------------
    # Calcul de la dérivée seconde (détecte les changements rapides).
    # Très sensible au bruit.
    lap_float = cv2.Laplacian(img_gray, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap_float)

    # ---------------------------------------------------------
    # 3. DÉTECTEUR DE CANNY
    # ---------------------------------------------------------
    # Algorithme multi-étapes (Gaussian -> Sobel -> Non-max suppression -> Hysteresis).
    # Utilise les valeurs des sliders définis par l'utilisateur.
    val_min = s_canny_min.val
    val_max = s_canny_max.val
    canny = cv2.Canny(img_gray, val_min, val_max)

    # ---------------------------------------------------------
    # MISE À JOUR DE L'AFFICHAGE
    # ---------------------------------------------------------
    
    # A. Image Originale
    ax_original.clear()
    ax_original.imshow(img_rgb)
    ax_original.set_title("1. Image Originale")
    ax_original.axis('off')
    
    # Nettoyage des autres axes
    ax_sobel.clear()
    ax_lap.clear()
    ax_canny.clear()

    # B. Affichage conditionnel (Superposition ou Brut)
    if etat_superposition:
        # Mode couleur : on dessine les contours en rouge sur l'image
        ax_sobel.imshow(superposer_contours(img_rgb, sobel))
        ax_sobel.set_title("2. Sobel (Superposé)")
        
        ax_lap.imshow(superposer_contours(img_rgb, lap))
        ax_lap.set_title("3. Laplacien (Superposé)")
        
        # Pour Canny, on crée un masque manuel
        sup_canny = img_rgb.copy()
        sup_canny[canny > 0] = [255, 0, 0] # Pixels de contour en Rouge
        ax_canny.imshow(sup_canny)
        ax_canny.set_title(f"4. Canny (Superposé)")
    else:
        # Mode N&B : on affiche juste le masque de contours
        ax_sobel.imshow(sobel, cmap='gray')
        ax_sobel.set_title("2. Sobel (Magnitude)")
        
        ax_lap.imshow(lap, cmap='gray')
        ax_lap.set_title("3. Laplacien")
        
        ax_canny.imshow(canny, cmap='gray')
        ax_canny.set_title(f"4. Canny")

    # On cache les axes (graduations) pour faire propre
    for ax in [ax_sobel, ax_lap, ax_canny]: 
        ax.axis('off')
        
    fig.canvas.draw_idle()

# =============================================================================
# 6. LANCEMENT
# =============================================================================

# Connexion des fonctions aux widgets
radio.on_clicked(update)
btn_superpo.on_clicked(basculer_superposition)
s_canny_min.on_changed(update)
s_canny_max.on_changed(update)
btn_bonus.on_clicked(ouvrir_fenetre_bonus)
btn_bonus_woaw.on_clicked(ouvrir_fenetre_bonus_woaw)

# Premier appel pour afficher la première image au démarrage
update()

plt.show()
