from urllib import response
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
movies=pd.read_csv('data_with_genre_better.csv')
ph=st.empty()

def get_movies_with_genre_or(moviedata=movies,genre=['Action','Thriller']):
	movielist=[]
	j=0
	for genreString in movies['genre']:
		i=0
		while genreString[i+1]!=']':
			g=""
			if i==0:
				i+=2
			else:
				i+=4
			while genreString[i]!="'":
				g+=genreString[i]
				i+=1
			for gen in genre:
				if g==gen:
					movielist.append(movies.iloc[j])
		j+=1
	df=pd.DataFrame(movielist)
	df=df.drop_duplicates()
	df=df.sort_values('score',ascending=False)
	return df

def get_movies_with_genre_and(moviedata=movies,genre=['Action','Thriller']):
	movielist=[]
	j=0
	for genreString in movies['genre']:
		i=0
		genList=[]
		while genreString[i+1]!=']':
			g=""
			if i==0:
				i+=2
			else:
				i+=4
			while genreString[i]!="'":
				g+=genreString[i]
				i+=1
			genList.append(g)
		if set(genre).issubset(set(genList)):
			movielist.append(movies.iloc[j])
		j+=1
	df=pd.DataFrame(movielist)
	df=df.drop_duplicates()
	df=df.sort_values('score',ascending=False)
	return df

def get_movies_with_prodcom_or(moviedata=movies,prodcom=['United Artists', 'Eon Productions']):
	movielist=[]
	j=0
	for prodString in movies['prod_comp']:
		i=0
		while prodString[i+1]!=']':
			p=""
			if i==0:
				i+=2
			else:
				i+=4
			while prodString[i]!="'":
				p+=prodString[i]
				i+=1
			for prod in prodcom:
				if p==prod:
					movielist.append(movies.iloc[j])
		j+=1
	df=pd.DataFrame(movielist)
	df=df.drop_duplicates()
	df=df.sort_values('score',ascending=False)
	return df


def get_movies_with_prodcom_and(moviedata=movies,prodcom=['United Artists', 'Eon Productions']):
	movielist=[]
	j=0
	for prodString in movies['prod_comp']:
		i=0
		prodList=[]
		while prodString[i+1]!=']':
			p=""
			if i==0:
				i+=2
			else:
				i+=4
			while prodString[i]!="'":
				p+=prodString[i]
				i+=1
			prodList.append(p)
		if set(prodcom).issubset(set(prodList)):
			movielist.append(movies.iloc[j])
		j+=1
	df=pd.DataFrame(movielist)
	df=df.drop_duplicates()
	df=df.sort_values('score',ascending=False)
	return df


def get_movies_with_lang(lang):
	return movies[movies['original_language']==lang]

st.title("Movie Recommender System")

all_movies=st.checkbox("Show all movies")

if all_movies:
	st.dataframe(movies[['id','title','genre','budget','vote_average']])
if not all_movies:
	ph.empty()
filter_movies=st.checkbox("Filter Movies")

if filter_movies:
	genre_recommend=st.checkbox("Find Best Movies according to Genre")
	lang_recommend=st.checkbox("Find Best Movies according to Language")
	prodcom_recommend=st.checkbox("Find Best Movies according to Production Company")

	if genre_recommend:
		recs=None

		genres=['Thriller','Music','Adventure','Comedy','Fantasy','Crime','History','Romance','Animation','Horror','Family','Mystery','Western','Drama','Science Fiction','Action','Documentary','War','TV Movie']
		
		cols=st.columns(2)

		for i,x in enumerate(cols):
			with x:
				if i==0:
					st.header("Choose filter mode")
					and_or=st.selectbox("",("Inclusive(And)","Exclusive(or)"))
				elif i==1:
					st.header("Select a Genre")
					gen=st.multiselect("",genres)

		
		if and_or=="Inclusive(And)":
			recs=get_movies_with_genre_and(genre=gen)
		if and_or=="Exclusive(or)":
			recs=get_movies_with_genre_or(genre=gen)

		recs=recs[['title','genre','score']]

		st.header("Top Movies for your Selected Genre")
		if recs is not None:
			st.dataframe(recs)

			x=list(movies['original_language'].value_counts()[:13].keys())


	elif lang_recommend:
		langs=['en', 'fr', 'ja', 'it', 'de', 'es', 'zh', 'sv', 'cn', 'fi', 'ru', 'ko', 'hi']
		langnc=['English','French','Japanese','Italian','German','Spanish','Chinese','Swedish','Mandarin','Finnish','Russian','Korean','Hindi']
		explode=[0,0,0,0,0,0,0,0,0,0,0,0,0]
		st.header("Choose a language")
		l=st.selectbox('',langnc)
		lx=l
		for i,x in enumerate(langnc):
			if x==l:
				l=langs[i]
				break

		for i,x in enumerate(langs):
			if langs[i]==l:
				explode[i]=0.1

		recs=get_movies_with_lang(l)
		st.title(f"Top {lx} movies")
		recs=recs[['title','genre','original_language','score']]
			


		st.dataframe(recs)
		# x=list(movies['original_language'].value_counts()[:13].keys())
		x=langnc
		y=list(movies['original_language'].value_counts()[:13])

		fig, ax = plt.subplots()
		ax.set_facecolor('pink')

		ax.pie(y,explode=explode,shadow=True)
		ax.legend(labels=x)
		st.pyplot(fig)

	elif prodcom_recommend:
		cols=st.columns(2)
		
		for i,x in enumerate(cols):
			with x:
				if i==0:
					st.header("Choose filter mode")
					and_or=st.selectbox("",("Inclusive(And)","Exclusive(or)"))
				elif i==1:
					st.header("Select a Production Company")
					prod=st.multiselect("",prodcoms)

		
		if and_or=="Inclusive(And)":
			recs=get_movies_with_prodcom_and(prodcom=prod)
		if and_or=="Exclusive(or)":
			recs=get_movies_with_prodcom_or(prodcom=prod)


		recs=recs[['title','genre','prod_comp','score']]

		st.header("Top Movies for your Selected Prod. Company")
		if recs is not None:
			st.dataframe(recs)
movie_recommend=st.checkbox("Recommend Me Movies!!!")

if movie_recommend:
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
			
			






footer="""<style>
.footer {
position:fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by Aditya Yadav & Ananya Karne</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)