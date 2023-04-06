import pickle
import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
from PIL import Image

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
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
    for i in distances[1:11]:
    
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('C:/Users/revan/Desktop/mini/movie_list.pkl','rb'))
similarity = pickle.load(open('C:/Users/revan/Desktop/mini/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("select a movie",movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5,col6,col7= st.columns(7)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0],use_column_width=True)
        st.write('           ')
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1],use_column_width=True)
        
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2],use_column_width=True)

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3],use_column_width=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4],use_column_width=True)
    with col6:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5],use_column_width=True)
    with col7:
        st.text(recommended_movie_names[6])
        st.image(recommended_movie_posters[6],use_column_width=True)
    
    


url = requests.get('https://assets4.lottiefiles.com/packages/lf20_puwecidm.json')

url_json = dict()

if url.status_code == 200:
	url_json = url.json()
else:
	print("Error in the URL")


st_lottie(url_json)

