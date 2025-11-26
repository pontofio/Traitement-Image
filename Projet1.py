import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider
import cv2
import os
import numpy as np

# --- 1. CONFIGURATION ---
dossier_img = 'images'
# On vérifie le dossier
if not os.path.exists(dossier_img):
    os.makedirs(dossier_img)
    print(f"Dossier '{dossier_img}' créé.")
    exit()

# On récupère les images
fichiers = [f for f in os.listdir(dossier_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if not fichiers:
    print("Aucune image trouvée.")
    exit()

# Si la liste est trop longue, on garde les 20 premières
if len(fichiers) > 20:
    fichiers = fichiers[:20]
    print("Attention : Liste tronquee aux 20 premiers fichiers.")

# --- 2. MISE EN PAGE (LAYOUT) ---
fig = plt.figure(figsize=(16, 9))

# A. Zone des Contrôles (Gauche)
rect_menu = [0.02, 0.4, 0.20, 0.55]   # Liste
rect_s1   = [0.05, 0.25, 0.15, 0.03]  # Slider 1
rect_s2   = [0.05, 0.15, 0.15, 0.03]  # Slider 2

# B. Zone des Images (Droite)
plt.subplots_adjust(left=0.30, right=0.98, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)

# --- 3. CRÉATION DES AXES D'IMAGES ---
ax_overlay = plt.subplot(2, 2, 1) # Haut Gauche
ax_sobel   = plt.subplot(2, 2, 2) # Haut Droite
ax_lap     = plt.subplot(2, 2, 3) # Bas Gauche
ax_canny   = plt.subplot(2, 2, 4) # Bas Droite

for ax in [ax_overlay, ax_sobel, ax_lap, ax_canny]:
    ax.axis('off')

# --- 4. CRÉATION DES WIDGETS ---

# Fond gris esthétique
fig.patches.extend([plt.Rectangle((0, 0), 0.28, 1, fill=True, color='#f0f0f0', alpha=1, zorder=-1, transform=fig.transFigure)])
fig.text(0.02, 0.96, "PANNEAU DE CONTROLE", fontsize=12, fontweight='bold', color='#333')

# A. Liste de choix
ax_radio = plt.axes(rect_menu, facecolor='#e8e8e8')
radio = RadioButtons(ax_radio, fichiers, active=0)

# B. Sliders
ax_seuil1 = plt.axes(rect_s1)
ax_seuil2 = plt.axes(rect_s2)
s_seuil1 = Slider(ax_seuil1, 'Seuil Min', 0, 255, valinit=100)
s_seuil2 = Slider(ax_seuil2, 'Seuil Max', 0, 255, valinit=200)

# --- 5. FONCTION DE TRAITEMENT ---
def update(val=None):
    # 1. Récupérer l'image choisie
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 2. Récupérer seuils
    th1 = s_seuil1.val
    th2 = s_seuil2.val

    # 3. Traitements
    # Sobel
    gx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(gx, gy)
    sobel = cv2.convertScaleAbs(sobel)

    # Laplacien
    lap = cv2.Laplacian(img_gray, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)

    # Canny
    canny = cv2.Canny(img_gray, int(th1), int(th2))

    # Superposition
    overlay = img_rgb.copy()
    overlay[canny > 0] = [255, 0, 0] 
    final_overlay = cv2.addWeighted(img_rgb, 0.7, overlay, 0.3, 0)

    # 4. Affichage
    ax_overlay.clear()
    ax_overlay.imshow(final_overlay)
    ax_overlay.set_title("1. Originale + Contours")
    ax_overlay.axis('off')

    ax_sobel.clear()
    ax_sobel.imshow(sobel, cmap='gray')
    ax_sobel.set_title("2. Sobel")
    ax_sobel.axis('off')

    ax_lap.clear()
    ax_lap.imshow(lap, cmap='gray')
    ax_lap.set_title("3. Laplacien")
    ax_lap.axis('off')

    ax_canny.clear()
    ax_canny.imshow(canny, cmap='gray')
    ax_canny.set_title(f"4. Canny ({int(th1)}, {int(th2)})")
    ax_canny.axis('off')

    fig.canvas.draw_idle()

# --- 6. CONNEXION ---
radio.on_clicked(update)
s_seuil1.on_changed(update)
s_seuil2.on_changed(update)

update()
plt.show()