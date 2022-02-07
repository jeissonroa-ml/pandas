import pandas as pd
pd.options.display.max_rows = 10
from urllib.parse import urlparse

df = pd.read_csv('eluniversal_2020_04_04_articles.csv')
df['newspaper_uid'] = 'el_universal'
df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

print(df['title'].value_counts())

df.drop_duplicates(subset=['title'], keep='first', inplace=True)