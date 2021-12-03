import pandas as pd
pd.options.display.max_rows = 10
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords 
#stopwords son palabras que no añaden importancia en un análisis de texto, p ej: el, la, etc

nltk.download('punkt') #se corre solo una vez
nltk.download('stopwords') #se corre solo una vez

df = pd.read_csv('eluniversal_2020_04_04_articles.csv')
df['newspaper_uid'] = 'el_universal'
df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

stop_words = set(stopwords.words('spanish'))

def tokenize_column(df, column_name):
    return(df
            .dropna()
            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1) #tokenizar
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens))) #eliminar palabras que no sean alfanúmericas
            .apply(lambda tokens: list(map(lambda token: token.lower(),tokens))) #combertir palabras en minus para poder compararlas
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list))) # eliminar palabras stop_words
            .apply(lambda valid_word: len(valid_word))
        )

df['tokens'] = tokenize_column(df, 'title')

print(df)