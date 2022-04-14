import streamlit as st

import pandas as pd

import numpy as np
st.set_page_config(layout="wide")
movies=pd.read_csv('data_with_genre_better.csv')
ph=st.empty()

def get_movies_with_genre(moviedata=movies,genre=['Action','Thriller']):
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
	return df

st.title("Movie Recommender System")

all_movies=st.checkbox("Show all movies")

if all_movies:
	st.dataframe(movies[['title','genre','budget','vote_average']])
if not all_movies:
	ph.empty()

genre_recommend=st.checkbox("Find Best Movies according to Genre")

if genre_recommend:
	genres=['Thriller','Music','Adventure','Comedy','Fantasy','Crime','History','Romance','Animation','Horror','Family','Mystery','Western','Drama','Science Fiction','Action','Documentary','War','TV Movie']
	gen=st.multiselect("Select a genre",genres)
	recs=get_movies_with_genre(genre=gen)
	recs=recs[['title','genre','score']]
	st.dataframe(recs)

