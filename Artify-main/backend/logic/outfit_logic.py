"""
ArtifyMe - AI Outfit Suggestion Logic (Color + Category Enhanced + Accurate)
Function:
  generate_single_outfit(image_path: str, category: str) -> dict

Returns a dict ready for JSON response:
{
  "category": "Party",
  "image": "/uploads/filename.jpg",
  "style": "Top Match",
  "description": "This pink outfit pairs perfectly with white or black bottoms, nude heels, and gold-plated accessories. Suits warm and cool skin tones."
}
"""

import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# -----------------------------
# Helper functions
# -----------------------------
def _basename(p: str) -> str:
    try:
        return os.path.basename(p)
    except Exception:
        return str(p)

def crop_foreground(image_path):
    """Crop image to remove bright background pixels"""
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    mask = np.all(data < 230, axis=2)  # ignore bright background
    coords = np.argwhere(mask)
    if coords.size == 0:
        return img  # fallback
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    return img.crop((x0, y0, x1, y1))

def dominant_color(image_path, n_colors=2):
    """Return dominant RGB colors using K-means, ignoring near-white/black background"""
    img = Image.open(image_path).convert('RGB').resize((100, 100))
    data = np.array(img).reshape(-1, 3)

    # Filter out near-white or near-black pixels
    data = np.array([pixel for pixel in data if not (
        all(channel > 240 for channel in pixel) or all(channel < 15 for channel in pixel)
    )])

    if len(data) == 0:
        data = np.array(img).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(data)
    counts = np.bincount(kmeans.labels_)

    # Sort clusters by frequency
    cluster_order = np.argsort(counts)[::-1]
    dominant_colors = [tuple(map(int, kmeans.cluster_centers_[i])) for i in cluster_order]

    # Return primary and secondary colors
    if len(dominant_colors) >= 2:
        return dominant_colors[0], dominant_colors[1]
    elif len(dominant_colors) == 1:
        return dominant_colors[0], None
    else:
        return (200, 200, 200), None  # fallback neutral

def closest_color_name(rgb):
    """Map RGB to human-readable color with expanded warm/pink shades"""
    COLORS = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "dark red": (139, 0, 0),
        "pink": (255, 192, 203),
        "peach": (255, 218, 185),
        "coral": (255, 127, 80),
        "salmon": (250, 128, 114),
        "rose": (207, 112, 110),
        "beige": (245, 245, 220),
        "blue": (0, 0, 255),
        "navy": (0, 0, 128),
        "green": (0, 128, 0),
        "lime": (50, 205, 50),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "dark orange": (255, 140, 0),
        "purple": (128, 0, 128),
        "lavender": (230, 230, 250),
        "maroon": (128, 0, 0),
        "brown": (165, 42, 42),
        "light brown": (181, 101, 29),
        "grey": (128, 128, 128),
        "silver": (192, 192, 192),
        "teal": (0, 128, 128),
        "cyan": (0, 255, 255),
        "neutral": (200, 200, 200)
    }
    r, g, b = rgb
    closest = min(COLORS.items(), key=lambda x: (x[1][0]-r)**2 + (x[1][1]-g)**2 + (x[1][2]-b)**2)
    return closest[0]

# -----------------------------
# Suggested color pairings
# -----------------------------
COLOR_PAIRINGS = {
    "white": "pair with any contrasting color for a fresh look. Suits all skin tones.",
    "black": "pair with bold colors or metallic accents. Universal skin tone friendly.",
    "red": "pair with black, white, or beige bottoms. Best for warm skin tones.",
    "pink": "pair with white, black, or beige bottoms. Suits warm and cool skin tones.",
    "peach": "pair with white, beige, or light brown bottoms. Suits warm and cool skin tones.",
    "rose": "pair with white, beige, or blush bottoms. Works well with warm and cool skin tones.",
    "coral": "pair with white, beige, or light brown bottoms. Complements warm skin tones.",
    "salmon": "pair with cream, tan, or white bottoms. Suits warm and cool skin tones.",
    "beige": "pair with brown, white, or pastel bottoms. Neutral and versatile.",
    "brown": "pair with white, beige, or pastel bottoms. Suits warm skin tones.",
    "maroon": "pair with white, beige, or gold-accented bottoms. Suits warm skin tones.",
    "blue": "pair with white, grey, or black bottoms. Suits all skin tones.",
    "navy": "pair with white, beige, or grey bottoms. Suits all skin tones.",
    "green": "pair with white, beige, or brown bottoms. Works well with warm tones.",
    "teal": "pair with white, beige, or black bottoms. Works with cool tones.",
    "yellow": "pair with white, denim, or grey bottoms. Suits cool skin tones.",
    "orange": "pair with white, denim, or beige bottoms. Warm skin tones shine.",
    "purple": "pair with white, black, or grey bottoms. Works with cool and warm tones.",
    "lavender": "pair with white, grey, or pastel bottoms. Works with cool skin tones.",
    "grey": "pair with black, white, or colored bottoms. Neutral pairing.",
    "neutral": "pair creatively with complementary or pastel colors."
}


# -----------------------------
# Accessory suggestions per category
# -----------------------------
CATEGORY_ACCESSORIES = {
    "casual": "Add sneakers, a crossbody bag, or simple necklace.",
    "sporty": "Add sneakers, sports cap, and wristband.",
    "office": "Add formal shoes, minimal jewelry, and a sleek watch.",
    "party": "Add heels, clutch, and statement jewelry.",
    "evening": "Add elegant clutch, subtle jewelry, and evening shoes.",
    "ethnic": "Add bangles, ethnic jewelry, and traditional footwear."
}

# -----------------------------
# Clothing type detection (simplified)
# -----------------------------
def detect_clothing_type(image_path):
    """Use filename keywords to detect type"""
    name = os.path.basename(image_path).lower()
    if any(x in name for x in ["shirt","top","blouse","tee","sweater","jacket","kurti"]):
        return "top"
    elif any(x in name for x in ["pant","jean","trouser","skirt","shorts","leggings","chinos","jogger"]):
        return "bottom"
    elif any(x in name for x in ["dress","gown","maxi","lehenga","saree"]):
        return "dress"
    elif any(x in name for x in ["shoe","sneaker","boot","heel","sandals","loafer","pump","flat"]):
        return "shoe"
    else:
        return "item"

# -----------------------------
# Main logic
# -----------------------------
def generate_single_outfit(image_path: str, category: str) -> dict:
    web_path = f"/uploads/{_basename(image_path)}"
    cat = (category or "General").strip().title()
    detected = detect_clothing_type(image_path)

    primary_rgb, secondary_rgb = dominant_color(image_path, n_colors=2)
    primary_color = closest_color_name(primary_rgb)
    secondary_color = closest_color_name(secondary_rgb) if secondary_rgb else None

    color_desc = COLOR_PAIRINGS.get(primary_color, "Pair creatively with complementary colors.")
    accessory_desc = CATEGORY_ACCESSORIES.get(category.lower(), "")

    # Style title
    style = f"{detected.capitalize()} Match"

    # Include secondary color in description if available
    secondary_text = f" Accent color {secondary_color} can be used in accessories." if secondary_color else ""

    description = f"This {primary_color} {detected} pairs perfectly with {color_desc}{secondary_text} {accessory_desc}".strip()

    return {
        "category": cat,
        "image": web_path,
        "style": style,
        "description": description
    }
