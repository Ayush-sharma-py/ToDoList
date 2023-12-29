import pandas
import nltk
from nltk import word_tokenize, pos_tag
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
 
# Download NLTK resources (only needed once)
#nltk.download('punkt')
#nltk.download('words')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
#nltk.download('wordnet')

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

    return " ".join(tokens)

stop = stopwords.words('english')
classes  = ["events", "personal", "work", "grocery"]

df = pandas.read_csv("ToDoList//data.csv")

for i in df.iloc[:,0]:
    print(sentenceProcessing(i))
