#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Reading Data 

# In[3]:


df= pd.read_csv('tripadvisor_hotel_reviews.csv')
#df.head()


# In[4]:


#df.isna().sum()


# In[5]:


#df.shape


# # Some Analysis

# In[6]:


#sns.countplot(x= df['Rating'])


# In[7]:


df['Word_count']= df['Review'].map(lambda x: len(x.split()))


# In[8]:


df.head()


# In[9]:


#sns.lineplot(x='Rating', data=df, y='Word_count')


# **Ingisht**
# * Higher Rated Reviews tend to have less words while, lower rated reviews have very high word count

# In[11]:


from textblob import TextBlob


# In[12]:


def polarity(text):
    blob= TextBlob(text)
    blob.sentiment
    polarity= blob.sentiment.polarity
    
    return polarity

def subjectivity(text):
    blob= TextBlob(text)
    blob.sentiment
    subjectivity= blob.sentiment.subjectivity
    
    return subjectivity


# In[13]:


df['Polarity']= df['Review'].apply(polarity)
df['Subjectivity']= df['Review'].apply(subjectivity)
#df


# In[14]:


#sns.distplot(df['Polarity'])


# In[15]:


#sns.distplot(df['Subjectivity'])


# In[16]:


#sns.boxplot(x='Rating',y='Polarity', data=df, whis=2.5, fliersize= 5)


# In[17]:


#sns.boxplot(x='Rating',y='Subjectivity', data=df, whis=2 )


# # Preprocessing the Data using SpaCy

# In[18]:


import spacy


# In[19]:


nlp= spacy.load('en_core_web_sm')


# In[23]:


def preprocess(text):
    lower= text.lower()
    doc= nlp(lower)
    tokens= [token.lemma_ for token in doc ]
    a_lemma= [lemma for lemma in tokens if lemma not in spacy.lang.en.stop_words.STOP_WORDS and lemma.isalpha()]
    return " ".join(a_lemma)


# In[24]:


df['Review_new']= df['Review'].apply(preprocess)


# In[ ]:


df


# In[ ]:


rev= " ".join([review for review in df['Review_new']])
rev[:2000]


# # WordCloud of 200 most occuring Words

# In[20]:


# from wordcloud import WordCloud
# plt.figure(figsize=(15,10))
# wc= WordCloud(max_words=200,height= 800, width=1000 ,background_color='black').generate(rev)
# plt.imshow(wc)


# In[21]:


def sentiment(review):
    if review>=3:
        return 1
    else:
        return 0
df['Sentiment']= df['Rating'].apply(sentiment)


# In[ ]:


df


# # Creating our Model

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk import word_tokenize


# In[ ]:


X= df['Review_new']
y= df['Sentiment']

X_train, X_test,y_train, y_test= train_test_split(X, y, test_size=0.25, stratify=y)


# In[ ]:


X_train


# In[ ]:


y_train


# In[ ]:


tfidf= TfidfVectorizer(max_features=10000, tokenizer= word_tokenize,ngram_range=(1,2) )
X_train_transformed= tfidf.fit_transform(X_train.values)
X_test_transformed= tfidf.transform(X_test.values)


# In[ ]:


X_train_transformed.shape


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

# rfc= RandomForestClassifier()
# rfc.fit(X_train_transformed, y_train)
# y_pred= rfc.predict(X_test_transformed)

# rfc.score(X_test_transformed, y_test)


# In[ ]:


from sklearn.linear_model import LogisticRegression

lr= LogisticRegression()
lr.fit(X_train_transformed, y_train)
y_pred= lr.predict(X_test_transformed)

lr.score(X_test_transformed, y_test)


# In[ ]:

import pickle
pickle.dump(lr,open("sentiment_model.sav","wb"))
pickle.dump(tfidf,open("tfidf.sav","wb"))


