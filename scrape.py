"""
Original: Victoria Schaller and Angela Wu 04/19/2023
Author: Alyssa DeMarco
Date: 04/26/2024
File: scrape.py
Purpose: reads the imported csv(s), cleans the text, applies sentiment, and saves out a usable copy of the data for main.py
"""
# imports
import pandas as pd
from afinn import Afinn
import nltk.corpus

# declaring the cleaning standards
stopwords_list = "english.txt"
punctuations = """!()-![]{};:,+'"\,<>./?@#$%^&*_~Â""" #List of punctuation to remove

# parses the text
def reviewTweet(review):
    splitReview = str(review).split() #Split the review into words
    parsedReview = " ".join([word.translate(str.maketrans('', '', punctuations)) + " " for word in splitReview]) #Takes the stubborn punctuation out
    return parsedReview #Returns the parsed review

# cleans the text using cleaning standards
def cleanTweet(review):
    clean_words = []
    splitReview = str(review).split()
    for w in splitReview:
        if w.isalpha() and w not in stopwords_list:
            clean_words.append(w.lower())
    clean_review = " ".join(clean_words)
    return clean_review

# applies a sentiment using Afinn
def sentiment(df):
    afinn = Afinn(language='en')
    # compute scores (polarity) and labels
    df['Sentiment'] = df['cleanText'].apply(afinn.score)
    return df

# call from main.py to parse, clean, and sentiment
def createImport(location):
    df = pd.read_csv(f'countries/{location}.csv')
    df['cleanText']=df['text'].apply(reviewTweet).apply(cleanTweet)
    df = sentiment(df)
    return df
