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

file_name = r"/Users/Noah/Desktop/tweetsDemo.csv"
dataset = pd.read_csv(file_name, sep= ',')
dataset = dataset.sample(frac=1).reset_index(drop=True)
print(dataset.head())
dataset.shape
dataset = dataset[['content']]
print(dataset.head())

# Create the dataframe that we are going to send back
df_to_transfer = pd.DataFrame(dataset, columns=['content'])
print("Data transfer")

print(df_to_transfer)

#Preprocessing that goes through the code turns everything to lowercase
#and gets rid of things that aren't letters or numbers
dataset['content'] =dataset['content'].apply(lambda x: x.lower())
dataset['content'] = dataset['content'].apply(lambda x: re.sub('[^a-zA-Z0-9\s]',"",x))
print(dataset['content'].head())

tokenizer_location = r"/Users/Noah/Desktop/data/tokenizer.pickle"

#Code to load the tokenizer
with open(tokenizer_location, 'rb') as handle:
    tokenizer = pickle.load(handle)

#Now convert the text to a set of arrays that represent the words
X = tokenizer.texts_to_sequences(dataset['content'].values)
X = pad_sequences(X, 54)
print(X[:7])

# #This turns the sentiment values positive, negative and neutral into vectors
# y = pd.get_dummies(dataset['sentiment']).values
# [print(dataset['sentiment'][i],y[i]) for i in range(0,7)]

#This is is to load the model once we have it and using it 
model = load_model(r"/Users/Noah/Desktop/LSTM/Sentiment/small_tweets.h5")

#This code does the predicting on a dataset
prediction = model.predict(X)
print(len(prediction))
print(prediction[:7])

#Variables used to create negative, neutral and positive from new dataset
prediction_sentiment = []

# This for loop goes through and properly classifies the vectors
for i in range(0,len(prediction)):
    # max_value = np.amax(prediction[i])
    max_index = np.where(prediction[i] == np.amax(prediction[i]))
    max_index = max_index[0][0]
    if max_index == 0:
        indicator = "Negative"
    elif max_index == 1:
        indicator = "Neutral"
    else:
        indicator = "Positive"
    prediction_sentiment.append(indicator)

#print(prediction_sentiment[:7])

# Add the predictions to this
df_to_transfer['Sentiment'] = prediction_sentiment

df_to_transfer.to_csv("finished_analysis.csv")