# 🎬 Movie Recommendation System

A full-stack AI movie recommendation platform that uses semantic embeddings and cosine similarity to recommend movies based on contextual understanding instead of simple keyword matching.

The system analyzes movie overview, genres, cast, keywords, and director information to generate highly relevant recommendations using Sentence Transformers.

---

# 🚀 Features

✅ Semantic AI-based movie recommendations  
✅ Sentence Transformer embeddings  
✅ Cosine similarity recommendation engine  
✅ FastAPI backend  
✅ Responsive modern frontend  
✅ Movie posters using TMDB API  
✅ Autocomplete search suggestions  
✅ Genre-based filtering  
✅ Fuzzy movie search matching  
✅ Similarity score for recommendations  
✅ REST API architecture  

---

# 🧠 How It Works

1. Movie metadata is cleaned and processed.
2. Important features are combined into a single `tags` column:
   - Overview
   - Genres
   - Keywords
   - Cast
   - Director
3. Sentence Transformer generates semantic embeddings.
4. Cosine similarity compares movie vectors.
5. FastAPI serves recommendations through API endpoints.
6. Frontend displays results with posters and filters.

---

# 🛠️ Tech Stack

## Backend
- Python
- FastAPI
- Pandas
- Scikit-learn
- Sentence Transformers
- Requests

## Frontend
- HTML
- CSS
- JavaScript

## APIs
- TMDB API

---

# 📂 Project Structure

```text
movie-recommender/
│
├── backend/
│   ├── main.py
│   ├── movies.pkl
│   ├── requirements.txt
│   ├── similarity.pkl
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│
├── notebook/
│   ├── movie_recommender_final.ipynb
│
├── screenshots/
│   ├── home.png
│   ├── results.png
│
├── README.md
```

---

# 📸 Screenshots

## Home Page

![Home Page](screenshots/home.png)

---

## Recommendation Results

![Recommendation Results](screenshots/results.png)

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

---

## 2️⃣ Backend Setup

```bash
cd backend
```

Create virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
python -m uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## 3️⃣ Frontend Setup

Open:

```text
frontend/index.html
```

using **Live Server** in VS Code.

---

# 🔌 API Endpoints

## GET `/movies`

Autocomplete movie suggestions.

### Example

```http
GET /movies?q=ava
```

---

## GET `/genres`

Returns all available genres.

---

## POST `/recommend`

Returns semantic movie recommendations.

### Example Request

```json
{
  "movie_name": "Avatar",
  "num_recommendations": 5,
  "genre_filter": "Action"
}
```

---

# 🧪 Example Output

```json
{
  "title": "Aliens",
  "similarity_score": 60.96,
  "genres": ["Horror", "Action", "ScienceFiction"]
}
```

## Live Demo

Frontend: https://YOUR_NETLIFY_URL.netlify.app

Backend API: https://movie-recommender-api-wawc.onrender.com

---

# 🧠 AI Concepts Used

- Semantic Embeddings
- NLP-based Recommendation Systems
- Cosine Similarity
- Sentence Transformers
- Vector Similarity Search
- Content-Based Filtering

---

# 📈 Future Improvements

- User authentication
- Personalized watchlists
- Collaborative filtering
- FAISS vector search
- User ratings and reviews
- Recommendation history
- Advanced filtering
- Deployment using Docker

---

# 👨‍💻 Author

Mokshit
