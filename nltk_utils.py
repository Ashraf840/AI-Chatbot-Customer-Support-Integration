import nltk
# Install "punkt" package while running nltk for the first time
# nltk.download("punkt")
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sent, all_words):
    tokenized_sent = [stem(w) for w in tokenized_sent]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for indx, w in enumerate(all_words):
        if w in tokenized_sent:
            bag[indx] = 1.0
    return bag



# # testing tokenization
# a = "am i speaking to a college staff?"
# print(a)    # Output: am i speaking to a college staff?
# a = tokenize(a)
# print(a)    # Output: ['am', 'i', 'speaking', 'to', 'a', 'college', 'staff', '?'

# b = ["Organize", "orGaNized", "organizing", "organizes"]
# stemmed_words = [stem(word) for word in b]
# print(stemmed_words)    # Output: ['organ', 'organ', 'organ', 'organ']
