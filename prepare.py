###imports

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

import re
import os
import json
from pprint import pprint

import unicodedata

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


import acquire as acq
import prepare as prep

###functions

def basic_clean(text):
    """
    This function takes in a string and applies some basic text cleaning to it:
    - Lowercase everything
    - Normalize unicode characters
    - Replace anything that is not a letter, number, whitespace or a single quote.
    """
    # Lowercase the text
    text = text.lower()
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Replace anything that is not a letter, number, whitespace or a single quote
    text = re.sub(r"[^a-z0-9\s']", '', text)
    
    return text

def tokenize(text):
    """
    This function takes in a string and tokenizes all the words in the string.
    """
    #create the tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    tokenize
    
    # Tokenize the text into string text
    text = tokenize.tokenize(text, return_str=True)
    return text

def stem(text):
    """
    This function takes in a string and applies stemming to all the words in the string.
    """
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Initialize the Porter stemmer
    stemmer = PorterStemmer()
    
    # Stem each word in the list of words
    stemmed_words = [stemmer.stem(word) for word in words]
    
    # Join the stemmed words back into a string
    stemmed_text = " ".join(stemmed_words)
    
    return stemmed_text

def lemmatize(text):
    """
    This function takes in a string and applies lemmatization to each word in the string.
    """
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Initialize the WordNet lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    # Lemmatize each word in the list of words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join the lemmatized words back into a string
    lemmatized_text = " ".join(lemmatized_words)
    
    return lemmatized_text

def remove_stopwords(text, extra_words=None, exclude_words=None):
    """
    This function takes in a string and removes all the stopwords from the string.
    It also accepts two optional parameters, extra_words and exclude_words, to include additional stop words and exclude specific words from removal.
    """
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Get the list of English stopwords from the NLTK corpus
    stopword_list = stopwords.words('english')
    
    # Add any extra stop words
    if extra_words:
        stopword_list += extra_words
    
    # Remove any exclude words from the stopword list
    if exclude_words:
        stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    # Remove the stopwords from the list of words
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join the filtered words back into a string
    filtered_text = " ".join(filtered_words)
    
    return filtered_text, stopword_list

def get_clean_news_articles():
    '''explanation'''
    
    topics = ['business', 'sports', 'technology', 'entertainment']

    final_list = acq.get_news_articles(topics)

    # turn that bad boy into a df

    final_df = pd.DataFrame(final_list)
    
    final_df = final_df.rename(columns={'content':'original'}).drop(columns='category')
    
    final_df['clean'] = final_df['original'].apply(prep.basic_clean)
    
    final_df['tokenized'] = final_df['clean'].apply(prep.tokenize)
    
    final_df['stemmed'] = final_df['tokenized'].apply(prep.stem)
    
    final_df['lemmatized'] = final_df['stemmed'].apply(prep.lemmatize)
    
    return final_df
