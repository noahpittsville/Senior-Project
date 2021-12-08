# Creator: Noah Pitts 
# This code is an extension of saStocks.py. Its purpose is to now apply the saved model
# and tokenizer to stock-tweets that are unlabeled. It will then classify these as
# positive, negative or neutral.

#Sentiment Analysis
import pickle
import keras_preprocessing
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

file_name = r"/Users/Noah/Desktop/data/labelled_tweets.csv"
dataset = pd.read_csv(file_name, sep= ';')
dataset = dataset.sample(frac=1).reset_index(drop=True)
print(dataset.head())
dataset.shape
dataset = dataset[['sentiment', 'text']]
dataset.head()

#This set of code goes through the code turns everything to lowercase
#and gets rid of things that aren't letters or numbers
dataset['text'].apply(lambda x: x.lower())
dataset['text'] = dataset['text'].apply(lambda x: re.sub('[^a-zA-Z0-9\s]',"",x))
print(dataset['text'].head())

tokenizer_location = r"/Users/Noah/Desktop/data/tokenizer.pickle"

#Code to load the tokenizer
with open(tokenizer_location, 'rb') as handle:
    tokenizer = pickle.load(handle)

#Now convert the text to a set of arrays that represent the words
X = tokenizer.texts_to_sequences(dataset['text'].values)
X = pad_sequences(X)
print(X[:7])

#This turns the sentiment values positive, negative and neutral into vectors
y = pd.get_dummies(dataset['sentiment']).values
[print(dataset['sentiment'][i],y[i]) for i in range(0,7)]

#This is is to load the model once we have it and using it 
model = load_model(r"/Users/Noah/Desktop/LSTM/Sentiment/small_tweets.h5")

# #Code to take a look under the hood to see what is predicting correctly and not correctly
# print(X_test)
# prediction = model.predict(X_test)
# [print(dataset['text'][i], prediction[i], y_test[i]) for i in range(0,7)]

#Code to attempt to test the entire data set rather than just one set of it
prediction = model.predict(X)
print(len(prediction))
print(prediction[:7])