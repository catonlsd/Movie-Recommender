const API_URL = "http://127.0.0.1:8000/recommend";
const MOVIES_URL = "http://127.0.0.1:8000/movies";
const GENRES_URL = "http://127.0.0.1:8000/genres";

const movieInput = document.getElementById("movieInput");
const suggestions = document.getElementById("suggestions");
const genreFilter = document.getElementById("genreFilter");

async function loadGenres() {
    try {
        const response = await fetch(GENRES_URL);
        const data = await response.json();

        data.genres.forEach(genre => {
            const option = document.createElement("option");
            option.value = genre;
            option.innerText = genre;
            genreFilter.appendChild(option);
        });

    } catch (err) {
        console.log("Could not load genres.");
    }
}

async function showSuggestions() {
    const query = movieInput.value.trim();

    suggestions.innerHTML = "";

    if (query.length < 2) {
        suggestions.classList.add("hidden");
        return;
    }

    try {
        const response = await fetch(`${MOVIES_URL}?q=${query}`);
        const data = await response.json();

        if (data.movies.length === 0) {
            suggestions.classList.add("hidden");
            return;
        }

        data.movies.forEach(movie => {
            const item = document.createElement("div");
            item.className = "suggestion-item";
            item.innerText = movie;

            item.addEventListener("click", function () {
                movieInput.value = movie;
                suggestions.classList.add("hidden");
            });

            suggestions.appendChild(item);
        });

        suggestions.classList.remove("hidden");

    } catch (err) {
        suggestions.classList.add("hidden");
    }
}

async function getRecommendations() {
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const results = document.getElementById("results");

    const movieName = movieInput.value.trim();
    const selectedGenre = genreFilter.value;

    results.innerHTML = "";
    error.classList.add("hidden");
    suggestions.classList.add("hidden");

    if (movieName === "") {
        error.innerText = "Please enter a movie name.";
        error.classList.remove("hidden");
        return;
    }

    loading.classList.remove("hidden");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_name: movieName,
                num_recommendations: 5,
                genre_filter: selectedGenre
            })
        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (!response.ok) {
            error.innerText = data.detail || "Something went wrong.";
            error.classList.remove("hidden");
            return;
        }

        if (data.recommendations.length === 0) {
            error.innerText = "No recommendations found for this genre filter.";
            error.classList.remove("hidden");
            return;
        }

        data.recommendations.forEach(movie => {
            const card = document.createElement("div");
            card.className = "movie-card";

            card.innerHTML = `
                ${
                    movie.poster
                    ? `<img src="${movie.poster}" class="poster" alt="${movie.title} poster">`
                    : ""
                }

                <h2 class="movie-title">${movie.title}</h2>

                <div class="score">
                    Similarity: ${movie.similarity_score}%
                </div>

                <p class="overview">
                    ${movie.overview}
                </p>

                <div class="info">
                    <span class="label">Genres:</span>
                    ${movie.genres.join(", ")}
                </div>

                <div class="info">
                    <span class="label">Cast:</span>
                    ${movie.cast.join(", ")}
                </div>

                <div class="info">
                    <span class="label">Director:</span>
                    ${movie.director.join(", ")}
                </div>
            `;

            results.appendChild(card);
        });

    } catch (err) {
        loading.classList.add("hidden");
        error.innerText = "Backend server is not running.";
        error.classList.remove("hidden");
    }
}

movieInput.addEventListener("input", showSuggestions);

movieInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        getRecommendations();
    }
});

document.addEventListener("click", function(event) {
    if (!event.target.closest(".input-wrapper")) {
        suggestions.classList.add("hidden");
    }
});

loadGenres();