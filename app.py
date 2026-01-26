import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None # Return None if poster not found or an error occurs

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        # fetch poster from API
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict_path = 'movies_dict.pkl'
similarity_path = 'similarity.pkl'

if not os.path.exists(movies_dict_path) or not os.path.exists(similarity_path):
    st.error("Model files not found. Please run the notebook to generate them.")
    st.stop()

try:
    movies_dict = pickle.load(open(movies_dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(similarity_path, 'rb'))
except (pickle.UnpicklingError, EOFError):
    st.error("Could not load model files. They may be corrupted.")
    st.stop()

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like',
    movies['title'].values
)

if st.button('Recommend Movies'):
    name, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        if posters[0]:
            st.image(posters[0])
    with col2:
        st.text(name[1])
        if posters[1]:
            st.image(posters[1])

    with col3:
        st.text(name[2])
        if posters[2]:
            st.image(posters[2])

    with col4:
        st.text(name[3])
        if posters[3]:
            st.image(posters[3])

    with col5:
        st.text(name[4])
        if posters[4]:
            st.image(posters[4])