# ArtifyMe Backend (Flask)

Beginner-friendly mock backend to serve outfit suggestions.

## Setup

1) Create and activate a virtual environment (Windows PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```
pip install -r requirements.txt
```

3) Run the server:

```
python app.py
```

The API will run on `http://127.0.0.1:5000`.

## API

- POST `/suggest_outfits`
  - Body: `multipart/form-data` with one or more `images` files
  - Response (mock):
  ```json
  {
    "outfits": [
      { "label": "Casual", "icon": "🧢", "imageUrl": "https://picsum.photos/..." },
      { "label": "Evening", "icon": "🌙", "imageUrl": "https://picsum.photos/..." }
    ]
  }
  ```

## Frontend Integration (example)

In your `index.html` JavaScript, after collecting `File` objects:

```js
const form = new FormData();
files.forEach(f => form.append('images', f));
fetch('http://127.0.0.1:5000/suggest_outfits', { method: 'POST', body: form })
  .then(r => r.json())
  .then(data => {
    // data.outfits -> render cards
  });
```

Replace the mock logic in `app.py` with TensorFlow/Keras model loading and predictions when ready.

