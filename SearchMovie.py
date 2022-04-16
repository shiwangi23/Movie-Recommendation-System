from urllib import response
import streamlit as st
import pandas as pd
import requests

movies=pd.read_csv("tmdb_5000_movies.csv")

def get_movie_id(movie_name):
	# st.write(int(movies[movies['title']==movie_name].id))
	return int(movies[movies['title']==movie_name].id)
def get_rating(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url
	response=requests.get(fetch_url)
	data=response.json()
	return data['vote_average']


def get_director(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits"
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url
	response=requests.get(fetch_url)
	data=response.json()
	for i in data['crew']:
		if i['known_for_department']=='Directing':
			return i['name']
def get_actors(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits"
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url
	response=requests.get(fetch_url)
	data=response.json()
	cast_list=[]
	for i in data['cast']:
		if i['known_for_department']=='Acting':
			cast_list.append(i['name'])
	return cast_list

def get_genre(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url
	response=requests.get(fetch_url)
	data=response.json()
	gen_list=[]
	for i in data['genres']:
		gen_list.append(i['name'])

	return gen_list
	


def fetch_poster(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url

	response=requests.get(fetch_url)
	data=response.json()
	poster_path="https://image.tmdb.org/t/p/w500/{}".format(data['poster_path'])
	return poster_path

def fetch_budget(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url

	response=requests.get(fetch_url)
	data=response.json()
	return data['budget']

def fetch_release_date(movie_id):
	fetch_url="https://api.themoviedb.org/3/movie/"+str(movie_id)
	api_url="?api_key=b1f4c14647b54d6f5b1a496ae02d486c&language=en-US"
	fetch_url+=api_url

	response=requests.get(fetch_url)
	data=response.json()
	return data['release_date']


def main():
	st.header("Search Movie")

	movie_selected=st.selectbox("",movies['title'])
	info=st.button("Get Movie Info")

	if info:
		st.header("Movie : {}".format(movie_selected))

		mov_id=get_movie_id(movie_selected)


		st.header("Director : {}".format(get_director(mov_id)))
		col1,col2,col3=st.columns(3)

		with col1:
			st.image(fetch_poster(mov_id))
		with col2:
			st.header("Cast : ")
			actor_data=pd.DataFrame()
			actor_data['Actor Name']=get_actors(mov_id)[:5]
			st.table(actor_data)
			st.header("Budget : {} Dollars".format(fetch_budget(mov_id)))
			st.header("Release Date : {}".format(fetch_release_date(mov_id)))


		with col3:
			st.header("Genres : ")
			genre_data=pd.DataFrame()
			genre_data['Genre']=get_genre(mov_id)
			st.table(genre_data)
			st.header("Rating : {}/10".format(get_rating(mov_id)))
			

