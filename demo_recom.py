from urllib import response
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import requests

movie_dataset=pd.read_csv("tmdb_5000_movies.csv")


cv=CountVectorizer(max_features=5000,stop_words='english')
new_df=pd.read_csv("stemmed_tags.csv")

vectors=cv.fit_transform(new_df['tags']).toarray()

similarity=cosine_similarity(vectors)

api_key="b1f4c14647b54d6f5b1a496ae02d486c"

def fetch_poster(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/{}?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US".format(movie_id)
	response=requests.get(fetch_url)
	data=response.json()
	poster_path="https://image.tmdb.org/t/p/w500/{}".format(data['poster_path'])
	return poster_path



def recommend(movie):
	movies=[]
	posters=[]
	movie_index=new_df[new_df['title']==movie].index[0]
	distances=similarity[movie_index]
	movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:11]
	for i in movies_list:
		movies_id=new_df.iloc[i[0]].movie_id
		posters.append(fetch_poster(movies_id))
		movies.append(new_df.iloc[i[0]].title)
	
	return movies,posters

st.title("Movie Name : ")
movie_name=st.selectbox("",new_df['title'])
recommend_me=st.button("Recommend Movies")

if recommend_me:
	st.header("Top 10 Similar Movies")

	movies,posters=recommend(movie_name)
	col1,col2,col3,col4,col5=st.columns(5)
	col6,col7,col8,col9,col10=st.columns(5)

	with col1:
		st.header(movies[0])
		st.image(posters[0])
	with col2:
		st.header(movies[1])
		st.image(posters[1])
	with col3:
		st.header(movies[2])
		st.image(posters[2])
	with col4:
		st.header(movies[3])
		st.image(posters[3])
	with col5:
		st.header(movies[4])
		st.image(posters[4])
	with col6:
		st.header(movies[5])
		st.image(posters[5])
	with col7:
		st.header(movies[6])
		st.image(posters[6])
	with col8:
		st.header(movies[7])
		st.image(posters[7])
	with col9:
		st.header(movies[8])
		st.image(posters[8])
	with col10:
		st.header(movies[9])
		st.image(posters[9])
		
		


# st.write(movies)

