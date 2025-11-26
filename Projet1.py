import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import cv2
import os
import numpy as np
#ok ok ok 
# --- 1. CONFIGURATION ---
dossier_img = 'images'
# Vérification du dossier
if not os.path.exists(dossier_img):
    os.makedirs(dossier_img)
    print(f"Dossier '{dossier_img}' créé.")
    exit()

# Récupération des images
fichiers = [f for f in os.listdir(dossier_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if not fichiers:
    print("Aucune image trouvée.")
    exit()

# Limite à 20 images pour l'affichage
if len(fichiers) > 20:
    fichiers = fichiers[:20]

# --- 2. MISE EN PAGE (INTERFACE) ---
fig = plt.figure(figsize=(16, 9))

# A. Zone de Gauche (Menu)
rect_menu = [0.02, 0.4, 0.20, 0.55] 

# B. Zone de Droite (Images)
plt.subplots_adjust(left=0.30, right=0.98, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)

# --- 3. PRÉPARATION DES 4 EMPLACEMENTS ---
# On prépare les 4 sous-graphiques vides pour la suite
ax_original = plt.subplot(2, 2, 1) # Haut Gauche
ax_sobel    = plt.subplot(2, 2, 2) # Haut Droite (Vide pour l'instant)
ax_lap      = plt.subplot(2, 2, 3) # Bas Gauche (Vide pour l'instant)
ax_canny    = plt.subplot(2, 2, 4) # Bas Droite (Vide pour l'instant)

# On enlève les axes (chiffres) partout pour faire propre
for ax in [ax_original, ax_sobel, ax_lap, ax_canny]:
    ax.axis('off')

# --- 4. CRÉATION DU MENU ---
# Fond gris à gauche
fig.patches.extend([plt.Rectangle((0, 0), 0.28, 1, fill=True, color='#f0f0f0', alpha=1, zorder=-1, transform=fig.transFigure)])
fig.text(0.02, 0.96, "CHOIX DE L'IMAGE", fontsize=12, fontweight='bold', color='#333')

# Liste des fichiers
ax_radio = plt.axes(rect_menu, facecolor='#e8e8e8')
radio = RadioButtons(ax_radio, fichiers, active=0)

# --- 5. FONCTION PRINCIPALE ---
def update(val=None):
    # 1. Récupérer le nom de l'image
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    
    # 2. Charger l'image
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    # On convertit en RGB pour l'affichage correct des couleurs
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # On convertit aussi en Gris (sera utile pour les futurs filtres)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 3. Affichage - Case 1 : Image Originale
    ax_original.clear()
    ax_original.imshow(img_rgb)
    ax_original.set_title("1. Image Originale")
    ax_original.axis('off')

    # 4. Nettoyage des autres cases (pour l'instant vides)
    ax_sobel.clear()
    ax_sobel.text(0.5, 0.5, "Emplacement Sobel", ha='center')
    ax_sobel.axis('off')

    ax_lap.clear()
    ax_lap.text(0.5, 0.5, "Emplacement Laplacien", ha='center')
    ax_lap.axis('off')

    ax_canny.clear()
    ax_canny.text(0.5, 0.5, "Emplacement Canny", ha='center')
    ax_canny.axis('off')

    # Rafraîchir l'écran
    fig.canvas.draw_idle()

# --- 6. LANCEMENT ---
radio.on_clicked(update) # On lie le clic à la fonction
update() # On lance une première fois
plt.show()