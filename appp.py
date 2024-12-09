import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit app header
st.header('Movie Recommender System')

# Load the pre-trained models
movies = pickle.load(open('/Users/monish/Documents/DS/CineMatch/FrontEnd/movie_list.pkl', 'rb'))
similarity = pickle.load(open('/Users/monish/Documents/DS/CineMatch/FrontEnd/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns for displaying recommendations
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
