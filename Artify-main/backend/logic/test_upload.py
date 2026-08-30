import requests
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Step 1: define the URL
url = "http://127.0.0.1:5000/generate_outfits"

# Step 2: correct the file paths (go one level up)
base_dir = os.path.dirname(__file__)
uploads_dir = os.path.join(base_dir, '..', 'uploads')

files = [
    ('images', open(os.path.join(uploads_dir, 'test1.jpg'), 'rb')),
    ('images', open(os.path.join(uploads_dir, 'test2.jpg'), 'rb'))
]

# Step 3: send POST request
response = requests.post(url, files=files)
print(response.json())
