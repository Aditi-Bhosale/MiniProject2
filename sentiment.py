#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[10]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[5]:


df=pd.read_csv('tripadvisor_hotel_reviews.csv')
df.head()


# In[6]:


# df.info()


# # In[7]:


# df.Rating.value_counts()


# # In[12]:


# from wordcloud import WordCloud
# plt.figure(figsize=(20,20))
# wc1 = WordCloud(max_words=2000, min_font_size=10, 
#                 height=800,width=1600,background_color="white").generate(" ".join(df[df["Rating"]==1].Review))
# plt.imshow(wc1)


# # In[13]:


# plt.figure(figsize=(20,20))
# wc5 = WordCloud(max_words=2000, min_font_size=10, 
#                 height=800,width=1600,background_color="white").generate(" ".join(df[df["Rating"]==5].Review))
# plt.imshow(wc5)


# # In[14]:


#function for cleaning Review
def standardize_text(df, field):
    df[field] = df[field].str.replace(r"http\S+", "")
    df[field] = df[field].str.replace(r"http","")
    df[field] = df[field].str.replace(r"@/S+","")
    df[field] = df[field].str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
    df[field] = df[field].str.replace(r"@"," at ")
    df[field] = df[field].str.lower()
    return df


# In[15]:


standardize_text(df,"Review")


# In[19]:


import re
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize


# In[21]:


#nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
corpus = []
for i in range(0, len(df)):
    review = re.sub('[^a-zA-Z]', ' ', df['Review'][i])
    review = review.split()
    review = [word for word in review if not word in set(stopwords.words('english'))]
    review = [lemmatizer.lemmatize(word) for word in review]
    review = ' '.join(review)
    corpus.append(review)


# In[22]:


corpus[:1]


# In[23]:


def sentiment(review):
    if review>=3:
        return 1
    else:
        return 0
df['Sentiment']= df['Rating'].apply(sentiment)


# In[25]:


nltk.download('punkt')


# In[26]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(ngram_range=(1, 3), max_features=10000, tokenizer = word_tokenize)
X = tfidf.fit_transform(corpus)
y = df['Sentiment']


# In[28]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X, y)


# In[ ]:

import pickle
pickle.dump(lr,open("sentiment_model.sav","wb"))
pickle.dump(tfidf,open("tfidf.sav","wb"))

