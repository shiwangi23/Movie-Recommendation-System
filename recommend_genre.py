import pandas as pd
import numpy as np

movies=pd.read_csv('data_with_genre_better.csv')

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

print(get_movies_with_genre())

		

