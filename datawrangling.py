import pandas as pd
pd.options.display.max_rows = 10

from urllib.parse import urlparse

el_universal = pd.read_csv('eluniversal_2020_04_04_articles.csv')

#añadimos una columna para tenerla como id

el_universal['newspaper_uid'] = 'el_universal'

#añadimos otra columna para obtener la url con otra libreria
#pandas permite integrar otras librerias o funciones

el_universal['host'] = el_universal['url'].apply(lambda url: urlparse(url).netloc)

print(el_universal)

# con el método value_counts() podemos hacer un conteo agrupado
print(el_universal['host'].value_counts())