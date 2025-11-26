import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
import cv2
import os
import numpy as np

# --- 1. CONFIGURATION ---
dossier_img = 'images'
if not os.path.exists(dossier_img):
    os.makedirs(dossier_img)
    print(f"Dossier '{dossier_img}' créé.")
    exit()

fichiers = [f for f in os.listdir(dossier_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if not fichiers:
    print("Aucune image trouvée.")
    exit()

if len(fichiers) > 20:
    fichiers = fichiers[:20]

# --- 2. MISE EN PAGE ---
fig = plt.figure(figsize=(16, 9))

# Définition des zones [left, bottom, width, height]
rect_menu = [0.02, 0.45, 0.20, 0.50]   # Liste des images (Haut Gauche)
rect_btn  = [0.05, 0.35, 0.15, 0.05]   # Bouton Superposition (Juste en dessous)

# Zone images (Droite)
plt.subplots_adjust(left=0.30, right=0.98, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)

# --- 3. PRÉPARATION DES AXES ---
ax_original = plt.subplot(2, 2, 1)
ax_sobel    = plt.subplot(2, 2, 2)
ax_lap      = plt.subplot(2, 2, 3)
ax_canny    = plt.subplot(2, 2, 4)

for ax in [ax_original, ax_sobel, ax_lap, ax_canny]:
    ax.axis('off')

# --- 4. WIDGETS ---
# Fond gris
fig.patches.extend([plt.Rectangle((0, 0), 0.28, 1, fill=True, color='#f0f0f0', alpha=1, zorder=-1, transform=fig.transFigure)])
fig.text(0.02, 0.96, "PANNEAU DE CONTRÔLE", fontsize=12, fontweight='bold', color='#333')

# A. Liste images
ax_radio = plt.axes(rect_menu, facecolor='#e8e8e8')
radio = RadioButtons(ax_radio, fichiers, active=0)

# B. Bouton Superposition
ax_btn = plt.axes(rect_btn)
btn_superpo = Button(ax_btn, 'Superposition : ON', color='lightblue', hovercolor='0.975')

# Variable d'état
etat_superposition = True 

# --- 5. FONCTIONS ---

def superposer_contours(image_rgb, masque_gris):
    """Crée l'image avec transparence"""
    contours_couleur = np.zeros_like(image_rgb)
    contours_couleur[:, :, 0] = masque_gris # Rouge
    return cv2.addWeighted(image_rgb, 1.0, contours_couleur, 0.8, 0)

def basculer_superposition(event):
    global etat_superposition
    etat_superposition = not etat_superposition
    
    if etat_superposition:
        btn_superpo.label.set_text('Superposition : ON')
        btn_superpo.color = 'lightblue'
    else:
        btn_superpo.label.set_text('Superposition : OFF')
        btn_superpo.color = 'white'
        
    update()

def update(val=None):
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)
    
    img_bgr = cv2.imread(chemin)
    if img_bgr is None: return
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # --- CALCULS ---
    # Sobel
    gx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.convertScaleAbs(cv2.magnitude(gx, gy))

    # Laplacien
    lap = cv2.convertScaleAbs(cv2.Laplacian(img_gray, cv2.CV_64F))

    # Canny (Valeurs fixes pour l'instant : 100 et 200)
    canny = cv2.Canny(img_gray, 100, 200)

    # --- AFFICHAGE ---
    
    # 1. Originale
    ax_original.clear()
    ax_original.imshow(img_rgb)
    ax_original.set_title("1. Originale")
    ax_original.axis('off')

    # 2, 3, 4 : Dépend du bouton
    ax_sobel.clear()
    ax_lap.clear()
    ax_canny.clear()

    if etat_superposition:
        # MODE SUPERPOSITION
        ax_sobel.imshow(superposer_contours(img_rgb, sobel))
        ax_sobel.set_title("2. Sobel (Superposé)")
        
        ax_lap.imshow(superposer_contours(img_rgb, lap))
        ax_lap.set_title("3. Laplacien (Superposé)")
        
        sup_canny = img_rgb.copy()
        sup_canny[canny > 0] = [255, 0, 0]
        ax_canny.imshow(sup_canny)
        ax_canny.set_title(f"4. Canny (Superposé)")
        
    else:
        # MODE BRUT
        ax_sobel.imshow(sobel, cmap='gray')
        ax_sobel.set_title("2. Sobel (Masque Brut)")
        
        ax_lap.imshow(lap, cmap='gray')
        ax_lap.set_title("3. Laplacien (Masque Brut)")
        
        ax_canny.imshow(canny, cmap='gray')
        ax_canny.set_title(f"4. Canny (Masque Brut)")

    for ax in [ax_sobel, ax_lap, ax_canny]: ax.axis('off')
    fig.canvas.draw_idle()

# --- 6. LIENS ---
radio.on_clicked(update)
btn_superpo.on_clicked(basculer_superposition)

update()
plt.show()