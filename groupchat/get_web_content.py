# filename: get_web_content.py

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Get the web content
url = "https://goodworkaround.com/2020/09/14/easiest-ways-to-get-an-access-token-to-the-microsoft-graph/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the main content of the webpage
text = soup.get_text()

# Tokenize the text
words = word_tokenize(text)

# Remove the stopwords
stopWords = set(stopwords.words("english"))
wordsFiltered = []

for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)

# Create a frequency table to keep the
# score of each word
freqTable = dict()
for word in wordsFiltered:
    word = word.lower()
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

# Create a dictionary to keep the score
# of each sentence
sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq

sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text
average = int(sumValues / len(sentenceValue))

# Store sentences into our summary.
summary = ''
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence

print(summary)