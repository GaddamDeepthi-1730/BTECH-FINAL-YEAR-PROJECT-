# ArtifyMe – AI Personal Style & Outfit Recommender

A full-stack AI-powered application that analyzes your wardrobe images and generates personalized outfit suggestions with style recommendations.

## 🎯 Features

- Upload wardrobe images (clothing items)
- AI-powered outfit analysis and categorization
- Personalized style recommendations
- Clean, modern pastel UI with smooth animations
- RESTful API backend with Flask

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Google Fonts (Poppins / Montserrat)
- Font Awesome icons
- Responsive design with modern UI/UX

### Backend
- Python 3.x
- Flask (REST API)
- TensorFlow (AI/ML models)
- NumPy, Pillow (Image processing)
- Flask-CORS (Cross-origin support)

## 📁 Project Structure

```
artify/
├── index.html              # Frontend application
├── backend/
│   ├── app.py             # Flask application
│   ├── logic/
│   │   ├── outfit_logic.py    # Outfit generation logic
│   │   └── imagenet_classes.txt
│   ├── uploads/           # User uploaded images
│   ├── requirements.txt   # Python dependencies
│   └── venv/              # Virtual environment (gitignored)
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. **Open `index.html` in your browser:**
   - Simply double-click `index.html`, or
   - Use a local server (recommended):
     ```bash
     # Using Python's built-in server
     python -m http.server 8000
     # Then visit http://localhost:8000
     ```

2. **Connect to Backend:**
   - Ensure the Flask backend is running on port 5000
   - The frontend will automatically connect to `http://127.0.0.1:5000`

## 📡 API Endpoints

### `POST /generate_outfits`

Generates outfit suggestions based on uploaded images.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `images` or `image`: Image file(s)
  - `category` (optional): Outfit category (e.g., "Casual", "Formal", "Party")

**Response:**
```json
{
  "category": "Casual",
  "image": "/uploads/filename.jpg",
  "style": "Suggested style title",
  "description": "Short suggestion text..."
}
```

### `GET /uploads/<filename>`

Serves uploaded images.

### `GET /`

Serves the frontend `index.html` or returns a success message.

## 🎨 Usage

1. **Start the backend server** (see Backend Setup above)
2. **Open the frontend** in your browser
3. **Upload wardrobe images** by clicking "Try Demo" or dragging images
4. **Click "Generate Outfit"** to get AI-powered suggestions
5. **View recommendations** with style labels and descriptions

## 🔧 Development

### Adding New Features

- **Backend logic**: Modify `backend/logic/outfit_logic.py`
- **API endpoints**: Add routes in `backend/app.py`
- **Frontend**: Edit `index.html` (JavaScript, CSS, HTML)

### Environment Variables

Create a `.env` file in the `backend/` directory for configuration:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📝 Notes

- Uploaded images are stored in `backend/uploads/` (gitignored)
- The application uses TensorFlow models for image classification
- All JavaScript is commented for educational purposes
- UI design emphasizes soft pastels, rounded corners, and subtle shadows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of a college project (2025).

## 🙏 Acknowledgments

- TensorFlow team for ML capabilities
- Flask community for the excellent framework
- Google Fonts for typography
