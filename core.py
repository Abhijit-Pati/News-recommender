import gensim.models as g
import nltk
import tensorflow
import codecs
import csv
import re
import string
import pandas as pd 
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def text_clean(A):
    l=len(A)
    C=[]
    for i in range(l):
        text=A[i]
        n=''
        for c in text:
            if c not in string.punctuation:
                n+=c
            else:
                n+=' '
        tokens = word_tokenize(n)
        tokens = [w.lower() for w in tokens]
        words = [word for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in words]
        text=' '.join(stemmed)
        C.append(text)
    return C

db= pd.read_csv('data/Corpus.csv',encoding='latin1')
content=db["Content"].tolist()
# title = db["Article Title"].tolist()
content=text_clean(content)
print(content[3])
model="data/apnews_dbow/doc2vec.bin"
output_file="data/ap_c_vectors.txt"


start_alpha=0.005
infer_epoch=1000


m = g.Doc2Vec.load(model)
content_docs = [ x.strip().split() for x in content ]

#infer test vectors
output = open(output_file, "w")
for d in content_docs:
    output.write( " ".join([str(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]) + "\n" )
output.flush()
output.close()

