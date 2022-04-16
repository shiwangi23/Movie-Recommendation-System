import pandas as pd
import numpy as np

movies=pd.read_csv('data_with_genre_better.csv')



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

print(get_movies_with_prodcom_or())

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

print(get_movies_with_prodcom_and())

		

