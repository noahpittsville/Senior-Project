#Sentiment Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import re
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding, Dropout
from keras.preprocessing.text import Tokenizer
#This helps deal with the different lengths
from keras.preprocessing.sequence import pad_sequences

dataset = pd.read_csv(r"/Users/Noah/Desktop/Tweets.csv")
dataset = dataset.sample(frac=1).reset_index(drop=True)
dataset.head()
dataset.shape
dataset = dataset[['airline_sentiment', 'text']]
dataset.head()

#This set of code goes through the code turns everything to lowercase
#and gets rid of things that aren't letters or numbers
dataset['text'].apply(lambda x: x.lower())
dataset['text'] = dataset['text'].apply(lambda x: re.sub('[^a-zA-Z0-9\s]',"",x))
dataset['text'].head()

#We only want to keep the most frequent represented by num_words
tokenizer = Tokenizer(num_words=5000, split= " ")
tokenizer.fit_on_texts(dataset['text'].values)

#Now convert the text to a set of arrays to train neural network
X = tokenizer.texts_to_sequences(dataset['text'].values)
X = pad_sequences(X)
print(X[:7])