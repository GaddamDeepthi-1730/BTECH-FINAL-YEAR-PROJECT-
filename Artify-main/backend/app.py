"""
ArtifyMe Backend - Flask Application

Handles a single uploaded image (and optional category), saves it to backend/uploads/,
generates one outfit suggestion via logic/outfit_logic.py, and returns JSON:

{
  "category": "Casual",
  "image": "/uploads/filename.jpg",
  "style": "Suggested style title",
  "description": "Short suggestion text..."
}

It can also serve the frontend `index.html` (if placed in the parent folder)
and exposes uploaded images via /uploads/<filename>.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from logic.outfit_logic import generate_single_outfit

# ------------------------------------------------------
# Basic paths and setup
# ------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Serve frontend from parent folder (adjust if index.html elsewhere)
app = Flask(__name__, static_folder="../", static_url_path="/")
CORS(app)


# ------------------------------------------------------
# Serve frontend
# ------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    """
    Serves index.html if available in the parent directory.
    If not found, responds with a simple text message.
    """
    try:
        return send_from_directory("../", "index.html")
    except Exception:
        return "✅ ArtifyMe backend running successfully.", 200


# ------------------------------------------------------
# Outfit Generation API
# ------------------------------------------------------
@app.route("/generate_outfits", methods=["POST"])
def generate_outfits():
    """
    Accepts:
      - form-data field 'images' (single file) or 'image'
      - optional form-data field 'category'

    Returns JSON:
    {
      "category": "...",
      "image": "/uploads/filename.jpg",
      "style": "...",
      "description": "..."
    }
    """
    # Get uploaded file (either 'images' or 'image')
    file = None
    if "images" in request.files:
        files = request.files.getlist("images")
        if files:
            file = files[0]
    elif "image" in request.files:
        file = request.files.get("image")

    if not file or file.filename == "":
        return jsonify({"error": "No image uploaded. Use form-data field 'images'."}), 400

    # Get optional category
    category = (
        request.form.get("category", "").strip()
        or request.args.get("category", "").strip()
        or "General"
    )

    # Save image
    filename = os.path.basename(file.filename)
    save_path = os.path.join(UPLOADS_DIR, filename)
    file.save(save_path)

    # Generate single outfit suggestion
    suggestion = generate_single_outfit(save_path, category)

    # Ensure proper path for frontend
    suggestion["image"] = f"/uploads/{filename}"

    return jsonify(suggestion), 200


# ------------------------------------------------------
# Serve uploaded images
# ------------------------------------------------------
@app.route("/uploads/<path:filename>", methods=["GET"])
def serve_uploads(filename):
    """Serves uploaded images from backend/uploads."""
    return send_from_directory(UPLOADS_DIR, filename)


# ------------------------------------------------------
# Run server
# ------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
