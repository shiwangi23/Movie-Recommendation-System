import streamlit as st

import pandas as pd

import numpy as np
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

st.title("Movie Recommender System")

all_movies=st.checkbox("Show all movies")

if all_movies:
	st.dataframe(movies[['title','genre','budget','vote_average']])
if not all_movies:
	ph.empty()

genre_recommend=st.checkbox("Find Best Movies according to Genre")

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