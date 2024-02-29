import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b88c7874470abc7c998dce307297b51e&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for 4xx or 5xx status codes
        data = response.json()
        poster_path = data.get('poster_path')  # Use .get() to safely access dictionary keys
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/original" + poster_path
            return full_path
        else:
            return None
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index
    if not index.empty:
        index = index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    else:
        return [], []

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, name in enumerate(recommended_movie_names):
        with globals()[f"col{i+1}"]:
            st.text(name)
            st.image(recommended_movie_posters[i])
