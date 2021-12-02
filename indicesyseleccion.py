import pandas as pd
pd.options.display.max_rows = 10 #nos muestra 10 datos en todos los df

el_universal = pd.read_csv('eluniversal_2020_04_04_articles.csv')
#print(el_universal)

# método dictionary like = df[ ]

print(el_universal['title'])
print(el_universal[['title', 'url']])

# método numpy like = df.iloc[ ]

print(el_universal.iloc[10:15])
print(el_universal.iloc[15]['url'])

# método label = df.loc[ ]

print(el_universal.loc[10:15,'body': 'title'])
#[filas, columnas] imprimir de la fila 10 a la fila 15 y de la columna body al title


