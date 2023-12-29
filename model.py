import pandas
import numpy as np
import nltk
from nltk import word_tokenize, pos_tag
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
 
# Download NLTK resources (only needed once)
#nltk.download('punkt')
#nltk.download('words')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
#nltk.download('wordnet')

filename = "data.csv"
classes  = ["events", "personal", "work", "grocery"]
df = pandas.read_csv(filename)

stop = stopwords.words('english')

def sentenceProcessing(sentence):
    # Lowercasing
    sentence = sentence.lower()

    # Removing stopwords
    sentence = ' '.join([word for word in sentence.split() if word not in stop])

    # Tokenize the sentence
    tokens = word_tokenize(sentence)

    # Removing the punctuations
    tokens = [word for word in tokens if word not in string.punctuation]

    # Lemmatizing
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(tokens)):
        tokens[i] = lemmatizer.lemmatize(tokens[i])

    return set(tokens)

def bagOfWords(vocab, sentence):
    arr = np.zeros(len(vocab))
    for i in range(0,len(vocab)):
        if vocab[i] in sentence:
            arr[i] = 1 # Change if adding duplicates

    return arr

vocab = set()
data = []

for i in range(0,len(df)):
    sentence = df.iloc[i,0]
    tokens = sentenceProcessing(sentence)
    data.append(tokens)
    vocab = vocab.union(tokens)

vocab = list(vocab)

# Use to debug the bag of words function
# print(vocab)
# for i in data:
#     print(bagOfWords(vocab,i))

trainInput = []
trainOutput = []
for i in data:
    trainInput.append(bagOfWords(vocab,i))
for i in df.iloc[:,1]:
    trainOutput.append(i)

trainInput = np.array(trainInput)
trainOutput = np.array(trainOutput)

# Training
X_train, X_test, y_train, y_test = train_test_split(trainInput, trainOutput, test_size=0.33, random_state=42)

# Model
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()

model.fit(X_train, y_train)

def predictTaskType(sentence):
    wordBag = bagOfWords(vocab,sentenceProcessing(sentence))
    ret = model.predict(np.array([wordBag]))
    return ret

predictedLabel = predictTaskType("Complete assigned readings")

print(classes[predictedLabel[0]])