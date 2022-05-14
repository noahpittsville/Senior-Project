# Creator: Noah Pitts 
# This code extends from SA, now applying the sentiment analysis to tweets regarding the stock market. 
# It then saves both the model and what is called the "tokenizer" (an object responsible for preprocessing the data)
# which can then later be called and applied on new data

#Sentiment Analysis
import pickle
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

#We only want to keep the most frequent represented by num_words
tokenizer = Tokenizer(num_words=5000, split= " ")
tokenizer.fit_on_texts(dataset['text'].values)

#save the tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer,handle,protocol=pickle.HIGHEST_PROTOCOL)

# tokenizer_location = r"/Users/Noah/Desktop/data/tokenizer.pickle"
tokenizer_location = r"/Users/Noah/Desktop/tokenizer.pickle"
# #Code to load the tokenizer
# with open(tokenizer_location, 'rb') as handle:
#     tokenizer = pickle.load(handle)

#Now convert the text to a set of arrays that represent the words
X = tokenizer.texts_to_sequences(dataset['text'].values)
X = pad_sequences(X)
print(X[:7])

#Now we do embedding layer
#This will convert the numbers within the array which is only
#a single number to vector space. This puts similar words close to one another
model = Sequential()
model.add(Embedding(5000, 256, input_length = X.shape[1]))

#We dropout 30%
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=True, dropout = 0.3, recurrent_dropout=0.2))
model.add(LSTM(256, dropout = 0.3, recurrent_dropout = 0.2))

#We use dense as 3 because there is positve, negative and neutral
model.add(Dense(3, activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

#This turns the sentiment values positive, negative and neutral into vectors
y = pd.get_dummies(dataset['sentiment']).values
[print(dataset['sentiment'][i],y[i]) for i in range(0,7)]

#This is the code involved in actually training the model
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state = 0)

batch_size = 32
epochs = 10

#This is the code that needs to be ran to fit the model
#print(model.fit(X_train, y_train, epochs = epochs, batch_size = batch_size, verbose = 2))

#This is to save the model
model.save(r"/Users/Noah/Desktop/small_tweets.h5")

#This is is to load the model once we have it and using it 

#Code to take a look under the hood to see what is predicting correctly and not correctly

prediction = model.predict(X_test)
[print(dataset['text'][i], prediction[i], y_test[i]) for i in range(0,7)]