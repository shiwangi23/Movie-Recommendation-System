import pandas as pd
import numpy as np

# moviemeta=pd.read_csv("movies_metadata.csv")

# minvotes=moviemeta['vote_count'].quantile(0.90)

# meanvotes=moviemeta['vote_count'].mean()

# q_movies=moviemeta.copy().loc[moviemeta['vote_count']>=minvotes]


# def weighted_avg_rating(x,minv=minvotes,meanv=meanvotes):
#     voters=x['vote_count']
#     avg_vote=x['vote_average']
#     leftside=(voters*avg_vote)/(voters+minv)
#     rightside=(minv*meanv)/(voters+minv)
    
#     return leftside+rightside

# q_movies['score']=q_movies.apply(weighted_avg_rating,axis=1)

# q_movies[['title','genres','vote_count','vote_average','score']].head(5)

# a=q_movies['genres']

# b=[]


# def get_only_names(s):
#     cleanar=[]
#     j=0
#     allow=True
#     while allow:
#         while s[j]!='n':
#             if s[j]==']':
#                 allow=False
#                 break
#             j+=1
#         if allow==False:
#             break
#         j+=8
#         newstr=""
#         while s[j]!="'":
#             newstr+=s[j]
#             j+=1
#         cleanar.append(newstr)
#     return cleanar


# for i in a:
#     b.append(get_only_names(i))

# c=[]
# for i in b:
#     newstr=""
#     for j in i:
#         newstr+=j
#         newstr+="|"
#     c.append(newstr)
        
# for i in range(0,len(c)):
#     c[i]=c[i][:-1]
    
# q_movies['genre']=c

# q_movies.genre=q_movies['genre'].str.split('|')

# q_movies.to_csv('data_with_genre_better.csv')

# genre_columns = list(set([j for i in q_movies['genre'].tolist() for j in i]))
# genre_columns=genre_columns[1:]


# for j in genre_columns:
#     q_movies[j] = 0
# for i in range(q_movies.shape[0]):
#     for j in genre_columns:
#         if(j in q_movies['genre'].iloc[i]):
#             q_movies.loc[i,j] = 1


# genres=['Thriller','Music','Adventure','Comedy','Fantasy','Crime','History','Romance','Animation','Horror','Family','Mystery','Western','Drama','Science Fiction','Action','Documentary','War','TV Movie']


# df=q_movies[q_movies["Family"]==1][['title','Family','genre','vote_count','vote_average','score']].sort_values('score',ascending=False).head(50)

# df.to_csv('out.csv')

def get_only_prodcom(s):
    cleanar=[]
    j=0
    allow=True
    while allow:
        while s[j]!='n':
            if s[j]==']':
                allow=False
                break
            j+=1
        if allow==False:
            break
        j+=8
        newstr=""
        while s[j]!="'":
            newstr+=s[j]
            j+=1
        cleanar.append(newstr)
    return cleanar
	
print(get_only_prodcom("[{'name': 'United Artists', 'id': 60}, {'name': 'Eon Productions', 'id': 7576}]"))

movies=pd.read_csv('data_with_genre_better.csv')

a=[]
for i in movies['production_companies']:
	a.append(i)
b=[]
for i in a:

	b.append(get_only_prodcom(i))

movies['prod_comp']=b

movies.to_csv('data_with_genre_better.csv')



