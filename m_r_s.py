from cProfile import label
import streamlit as st

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

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

def get_movies_with_lang(lang):
	return movies[movies['original_language']==lang]

st.title("Movie Recommender System")

all_movies=st.checkbox("Show all movies")

if all_movies:
	st.dataframe(movies[['title','genre','budget','vote_average']])
if not all_movies:
	ph.empty()

genre_recommend=st.checkbox("Find Best Movies according to Genre")
lang_recommend=st.checkbox("Find Best Movies according to Language")

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

	st.dataframe(recs)
	# x=list(movies['original_language'].value_counts()[:13].keys())
	x=langnc
	y=list(movies['original_language'].value_counts()[:13])

	fig, ax = plt.subplots()
	ax.set_facecolor('pink')

	ax.pie(y,explode=explode,shadow=True)
	ax.legend(labels=x)
	st.pyplot(fig)



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