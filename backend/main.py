import os
import pickle
import difflib
import logging
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOVIES_PATH = "movies.pkl"
SIMILARITY_PATH = "similarity.pkl"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

movies = None
similarity = None


def load_data():
    global movies, similarity

    if not os.path.exists(MOVIES_PATH) or not os.path.exists(SIMILARITY_PATH):
        return False

    with open(MOVIES_PATH, "rb") as f:
        movies = pickle.load(f)

    with open(SIMILARITY_PATH, "rb") as f:
        similarity = pickle.load(f)

    return True


def fetch_movie_poster(movie_title):
    try:
        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={TMDB_API_KEY}"
            f"&query={movie_title}"
        )

        response = requests.get(url)
        data = response.json()

        results = data.get("results")

        if results:
            poster_path = results[0].get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except:
        return None


class RecommendationRequest(BaseModel):
    movie_name: str
    num_recommendations: int = 5
    genre_filter: str | None = None


@app.on_event("startup")
async def startup_event():
    if load_data():
        logging.info("Movie data loaded successfully.")
    else:
        logging.warning("movies.pkl or similarity.pkl missing.")


@app.get("/")
def home():
    return {
        "message": "AI Movie Recommender API running successfully."
    }


@app.get("/movies")
def get_movie_titles(q: str = Query(default="")):
    if movies is None:
        if not load_data():
            raise HTTPException(status_code=500, detail="Model files not found.")

    titles = movies["title"].tolist()

    if not q:
        return {"movies": titles[:20]}

    matches = [
        title for title in titles
        if q.lower() in title.lower()
    ]

    return {"movies": matches[:10]}


@app.get("/genres")
def get_genres():
    if movies is None:
        if not load_data():
            raise HTTPException(status_code=500, detail="Model files not found.")

    all_genres = set()

    for genre_list in movies["genres"]:
        for genre in genre_list:
            all_genres.add(genre)

    return {
        "genres": sorted(list(all_genres))
    }


@app.post("/recommend")
def recommend_movies(request: RecommendationRequest):
    if movies is None or similarity is None:
        if not load_data():
            raise HTTPException(
                status_code=500,
                detail="Model files not found."
            )

    movie_name = request.movie_name.strip()

    if movie_name == "":
        raise HTTPException(
            status_code=400,
            detail="Movie name cannot be empty."
        )

    titles = movies["title"].tolist()

    matches = difflib.get_close_matches(
        movie_name,
        titles,
        n=1,
        cutoff=0.4
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{movie_name}' not found."
        )

    selected_movie = matches[0]

    movie_index = movies[
        movies["title"] == selected_movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:100]

    recommendations = []

    for i in movie_list:
        movie_data = movies.iloc[i[0]]

        if request.genre_filter and request.genre_filter != "All":
            if request.genre_filter not in movie_data["genres"]:
                continue

        recommendations.append({
            "title": movie_data["title"],
            "similarity_score": round(float(i[1]) * 100, 2),
            "overview": " ".join(movie_data["overview"]),
            "genres": movie_data["genres"],
            "cast": movie_data["cast"],
            "director": movie_data["crew"],
            "poster": fetch_movie_poster(movie_data["title"])
        })

        if len(recommendations) == request.num_recommendations:
            break

    return {
        "input_movie": selected_movie,
        "genre_filter": request.genre_filter or "All",
        "recommendations": recommendations
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )