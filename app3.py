import streamlit as st
import pickle
import pandas as pd
import requests

# 🔹 Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiODVjNmQwNzJhZDcyZjVjNjUxZGIxMjg5YTIwMmFjMCIsIm5iZiI6MTc1MjU4NDI4My4yMjUsInN1YiI6IjY4NzY1MDViYTMxZTZmZjJjMDdjNTM2ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.PXrZf_sCnANe6JXgomlX1L31JLL0BMXkuI7iVlhRkvE',
        'accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/original{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for movie_id {movie_id}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error for movie_id {movie_id}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error for movie_id {movie_id}: {timeout_err}")
    except Exception as err:
        print(f"Unknown error for movie_id {movie_id}: {err}")

    return "https://via.placeholder.com/300x450?text=Error"

# 🔹 Recommendation Logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id_x']
        title = movies.iloc[i[0]]['title']
        poster = fetch_poster(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# 🔹 Load Data
movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# 🔹 Streamlit App UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Choose a movie to get similar recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.subheader("Top 5 Recommended Movies:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)
