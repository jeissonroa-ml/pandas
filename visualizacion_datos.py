import pandas as pd
pd.options.display.max_rows = 10
from urllib.parse import urlparse

df = pd.read_csv('eluniversal_2020_04_04_articles.csv')
df['newspaper_uid'] = 'el_universal'
df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

print(df.describe())

#%matplotlib inline
df['n_tokens_title'].plot(style = 'k.')
df['n_tokens_body'].plot(style = 'r.')

#..ver miro