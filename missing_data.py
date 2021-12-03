import pandas as pd
pd.options.display.max_rows = 10
from urllib.parse import urlparse

df = pd.read_csv('eluniversal_2020_04_04_articles.csv')

df['newspaper_uid'] = 'el_universal'

df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)


#Rellenar datos faltantes
# Creamos una máscara con TRUE si tiene Nan o FALSE si tiene datos
missing_titles_mask = df['title'].isna()


#Panda permite filtrar datos verdaderos pasándole una lista
#df[máscara_escoge_valores_TRUE][columna del df].str.extract(expresión regular)
missing_titles = (df[missing_titles_mask]['url']
                    .str.extract(r'(?P<Missing_titles>[^/]+)$')
                    .applymap(lambda title: title.split('-')) #Crea una lista dividiendola por los guiones
                    .applymap(lambda title_word_list: ' '.join(title_word_list)))