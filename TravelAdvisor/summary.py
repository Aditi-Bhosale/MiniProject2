import sys

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np

import networkx as nx

def read_article(file_name):
    file=open(file_name,"r",encoding='utf-8')
    filedata=file.readlines()
    article=filedata[0].split(". ")
    sentences=[]
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z"," ").split(" "))
    sentences.pop()

    return sentences


def sentences_similarity(sent1,sent2,stopwords=None):
    if stopwords is None:
        stopwords=[]
    sent1=[w.lower() for w in sent1]
    sent2=[w.lower() for w in sent2]
    all_words=list(set(sent1+sent2))

    vector1=[0]*len(all_words)
    vector2=[0]*len(all_words)

    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)]+=1

    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)]+=1

    return 1-cosine_distance(vector1,vector2)

def gen_sim_matrix(sentences,stop_words):
    sim_matrix=np.zeros((len(sentences),len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if(i==j):
                continue
            sim_matrix[i][j]=sentences_similarity(sentences[i],sentences[j],stop_words)

    return sim_matrix

def gen_summary(file_name,top_n):
    stop_words=stopwords.words('english')
    summarize_text=[]
    sentences=read_article(file_name)
    sen_sim_matrix=gen_sim_matrix(sentences,stop_words)
    sen_sim_graph=nx.from_numpy_array(sen_sim_matrix)
    scores=nx.pagerank(sen_sim_graph)
    ranked_sen=sorted(((scores[i],s)for i,s in enumerate(sentences)),reverse=True)

    l=len(ranked_sen)
    for i in range(top_n):
        if(l==0):
            break
        summarize_text.append(" ".join(ranked_sen[i][1]))
        l=l-1
    #text_data="Summary :",". ".join(summarize_text).encode("utf-8")
    print("Summary :",". ".join(summarize_text).encode("utf-8"))
    #print(text_data.decode("utf-8"))

    #return "Summary :",". ".join(summarize_text)

print('The summary of %s is '%(sys.argv[1]))
loc=(sys.argv[1])+".txt"
# print(type(loc))
gen_summary(loc,5)


