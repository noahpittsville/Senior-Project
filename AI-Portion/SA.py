# Creator: Noah Pitts
# This code provides the intial set up to the project. This code creates a sentiment analysis model 
# using tweets regarding airlines. The tweets from the dataset have all been labeled as positive,
# negative or netural

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
print(dataset['text'].head())

#We only want to keep the most frequent represented by num_words
tokenizer = Tokenizer(num_words=5000, split= " ")
tokenizer.fit_on_texts(dataset['text'].values)

#Now convert the text to a set of arrays that represent the words
X = tokenizer.texts_to_sequences(dataset['text'].values)
X = pad_sequences(X)
print(X[:7])

# #Now we do embedding layer
# #This will convert the numbers within the array which is only
# #a single number to vector space. This puts similar words close to one another
# model = Sequential()
# model.add(Embedding(5000, 256, input_length = X.shape[1]))

# #We dropout 30%
# model.add(Dropout(0.3))
# model.add(LSTM(256, return_sequences=True, dropout = 0.3, recurrent_dropout=0.2))
# model.add(LSTM(256, dropout = 0.3, recurrent_dropout = 0.2))

# #We use dense as 3 because there is positve, negative and neutral
# model.add(Dense(3, activation = 'softmax'))
# model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())

y = pd.get_dummies(dataset['airline_sentiment']).values
[print(dataset['airline_sentiment'][i],y[i]) for i in range(0,7)]

#This is the code involved in actually training the model
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state = 0)

batch_size = 32
epochs = 10

#This is the code that needs to be ran to fit the model

#print(model.fit(X_train, y_train, epochs = epochs, batch_size = batch_size, verbose = 2))

#This is to save the model
#model.save(r"/Users/Noah/Desktop/LSTM/Sentiment/Sentiment_Model.h5")

#Load the model
model = load_model(r"/Users/Noah/Desktop/LSTM/Sentiment/Sentiment_Model.h5")

#Code to take a look under the hood to see what is predicting correctly and not correctly

prediction = model.predict(X_test)
[print(dataset['text'][i], prediction[i], y_test[i]) for i in range(0,7)]