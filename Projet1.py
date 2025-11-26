import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import cv2
import os
import numpy as np

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

# Limite à 50 images (au lieu de 20)
if len(fichiers) > 50:
    fichiers = fichiers[:50]

# --- 2. MISE EN PAGE ---
fig = plt.figure(figsize=(16, 9))

# A. Zone de gauche (Menu)
rect_menu = [0.02, 0.4, 0.20, 0.55]

# B. Zone de droite (Images)
plt.subplots_adjust(left=0.30, right=0.98, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)

# --- 3. PRÉPARATION DES 4 EMPLACEMENTS ---
ax_original = plt.subplot(2, 2, 1)
ax_sobel    = plt.subplot(2, 2, 2)
ax_lap      = plt.subplot(2, 2, 3)
ax_canny    = plt.subplot(2, 2, 4)

for ax in [ax_original, ax_sobel, ax_lap, ax_canny]:
    ax.axis('off')

# --- 4. CRÉATION DU MENU AVEC FOND ---
fig.patches.extend([
    plt.Rectangle((0, 0), 0.28, 1, fill=True, color='#f0f0f0', alpha=1, zorder=-1, transform=fig.transFigure)
])
fig.text(0.02, 0.96, "CHOIX DE L'IMAGE", fontsize=12, fontweight='bold', color='#333')

# --- SYSTÈME SCROLLABLE POUR RADIOBUTTONS ---
visible_count = 7  # Nombre d'éléments visibles dans la liste
offset = 0         # Position de scroll

def get_visible_items():
    return fichiers[offset : offset + visible_count]

# Création de la zone
ax_radio = plt.axes(rect_menu, facecolor='#e8e8e8')

# RadioButtons initiaux
radio = RadioButtons(ax_radio, get_visible_items(), active=0)

# --- 5. FONCTION PRINCIPALE ---
def update(val=None):
    nom_image = radio.value_selected
    chemin = os.path.join(dossier_img, nom_image)

    img_bgr = cv2.imread(chemin)
    if img_bgr is None:
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Image originale
    ax_original.clear()
    ax_original.imshow(img_rgb)
    ax_original.set_title("1. Image Originale")
    ax_original.axis('off')

    # Placeholders
    for ax, txt in [(ax_sobel, "Emplacement Sobel"),
                    (ax_lap, "Emplacement Laplacien"),
                    (ax_canny, "Emplacement Canny")]:
        ax.clear()
        ax.text(0.5, 0.5, txt, ha='center')
        ax.axis('off')

    fig.canvas.draw_idle()

# --- SCROLL AVEC MOLETTE ---
def on_scroll(event):
    global offset, radio

    if event.inaxes != ax_radio:
        return

    # Scroll vers le haut
    if event.button == 'up' and offset > 0:
        offset -= 1

    # Scroll vers le bas
    elif event.button == 'down' and offset < len(fichiers) - visible_count:
        offset += 1

    # Mise à jour du widget
    ax_radio.clear()
    new_items = get_visible_items()
    radio = RadioButtons(ax_radio, new_items, active=0)
    radio.on_clicked(update)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("scroll_event", on_scroll)

# --- 6. LANCEMENT ---
radio.on_clicked(update)
update()
plt.show()
