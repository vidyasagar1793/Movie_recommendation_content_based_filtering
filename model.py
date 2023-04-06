#!/usr/bin/env python
# coding: utf-8

# In[160]:


import numpy as np
import pandas as pd
import ast


# In[161]:


movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')


# In[162]:


movies.head()


# In[163]:


movies.shape


# In[164]:


credits.head()


# In[165]:


credits.head()


# In[166]:


movies=movies.merge(credits,on='title')
movies.head()


# In[167]:


movies.info()


# In[168]:


movies=movies[['id','title','overview','genres','keywords','crew','cast']]


# In[169]:


movies.head(34)


# In[170]:


movies.isnull().sum()


# In[171]:


movies.iloc[0].genres


# In[172]:


def convert(obj):
    if isinstance(obj, list):
        return obj
    try:
        L = []
        for i in ast.literal_eval(obj):
            if 'name' in i:
                L.append(i['name'])
            else:
                print(f"Dictionary {i} does not have a 'name' key")
        return L
    except ValueError as e:
        print(f"Failed to convert {obj} to a list of dictionaries: {e}")


# In[173]:


movies['genres']=movies['genres'].apply(convert)


# In[174]:


movies.head(3)


# In[175]:


movies['keywords']=movies['keywords'].apply(convert)


# In[176]:


movies.head()


# In[177]:


movies['cast'][0]


# In[178]:


def convert3(obj):
    L=[]
    count=0
    for i in ast.literal_eval(obj):
        if count!=3:
            L.append(i['name'])
            count += 1
        else:
            break
    return L


# In[179]:


movies['cast']=movies['cast'].apply(convert3)


# In[180]:


movies['cast'][0]


# In[181]:


movies.head()


# In[ ]:





# In[182]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


# In[183]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[184]:


movies.head(5)


# In[185]:


movies['overview'][567]


# In[ ]:





# In[186]:



print(movies['overview'].isnull().sum())

movies['overview'] = movies['overview'].fillna('')

movies['overview'] = movies['overview'].apply(lambda x: x if isinstance(x, list) else x.split())


# In[187]:


movies.head()


# In[188]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[189]:


movies.head()


# In[190]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])


# In[191]:


movies.head()


# In[192]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[193]:


movies['tags'][0]


# In[194]:


newtable=movies[['id','title','tags']]


# In[195]:


newtable.head(10)


# In[196]:


#newtable['tags'] = newtable['tags'].apply(lambda x:" ".join(x))
newtable['tags'][0]


# In[197]:


newtable['tags'][0]


# In[198]:


newtable['tags'][569]


# In[204]:


newtable['tags'] = newtable['tags'].astype(str).apply(lambda x: x.lower())


# In[205]:


newtable['tags'][477]


# In[201]:


#from sklearn.feature_extraction.text import CountVectorizer
#cv=CountVectorizer(max_features=5000,stop_words='english')


# In[202]:


#cv.fit_transform(newtable['tags']).toarray()


# In[211]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv=CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(newtable['tags'])


# In[245]:


similarity = cosine_similarity(vector)
print(similarity)


# In[208]:


#def get_title_from_index(index):
#    return df[df.index == index]["title"].values[0]
#def get_index_from_title(title):
#    return df[df.title == title]["id"].values[0]


# In[ ]:


#movie_user_likes = "Star Trek Beyond"
#movie_index = get_index_from_title(movie_user_likes)
#similar_movies = list(enumerate(cosine_sim[movie_index]))


# In[223]:


newtable[newtable['title'] == 'The Lego Movie'].index[0]


# In[242]:


def recommend(movie):
    index = newtable[newtable['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:11]:
        print(newtable.iloc[i[0]].title)
        


# In[243]:


recommend('Spectre')


# In[247]:


import pickle
pickle.dump(newtable,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

