
import numpy as np
from nltk.stem.porter import PorterStemmer
import underthesea

Stemmer = PorterStemmer()

def tokenize(sentence):
    return underthesea.word_tokenize(sentence)

def lower(word):
    return word.lower()

def stem(word):
    return Stemmer.stem(word.lower())
    
def bag_of_words(tokenized_sentence,words): # chuyen du lieu sang dang vector
    
    sentence_word = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words),dtype = np.float32)

    for idx ,w in enumerate(words):
        if w in sentence_word:
            bag[idx] = 1

    return bag
