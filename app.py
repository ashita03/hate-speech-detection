# Streamlit application for hate speech detection

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import string
import nltk
import re
from nltk.util import pr
from nltk.corpus import stopwords

import pandas as pd
import numpy as np
import string

nltk.download('stopwords')
stopword = set(stopwords.words('english'))


data = pd.read_csv('data/hate-speech.csv')
# print(data.head())

data["labels"] = data["class"].map(
    {0: "Hate Speech", 1: "Offensive Language", 2: "No Hate and Offensive"})
# print(data.head())

data = data[["tweet", "labels"]]
# print(data.head())

stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))


def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text


data["tweet"] = data["tweet"].apply(clean)
# print(data.head())

x = np.array(data["tweet"])
y = np.array(data["labels"])

cv = CountVectorizer()
X = cv.fit_transform(x)  # Fit the Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)


def hate_speech_detection():
    import streamlit as st
    st.title("Hate Speech Detection")
    user_entry = st.text_area("Enter any Tweet: ")
    if len(user_entry) < 1:
        st.write("  ")
    else:
        sample = user_entry
        data = cv.transform([sample]).toarray()
        a = clf.predict(data)
        st.title(a)


hate_speech_detection()
