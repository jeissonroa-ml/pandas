
import pandas as pd
pd.options.display.max_rows = 10
from urllib.parse import urlparse
# 4 Añadir uid a las filas
import hashlib  # Libreria dentro de libreria estandar, para operaciones criptograficas
# Numero unico para poder identificar a nuestra fila

df = pd.read_csv('eluniversal_2020_04_04_articles.csv')

df['newspaper_uid'] = 'el_universal'

df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)


uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            # Aplicamos la funcion a las filas (axis=1). La función md5 de la librería hashlib no debe ser utilizada para criptografia. Lo utilizamos porque nos puede dar un identificador unico. Nos da un numero de 128 bytes que lo vamos a representar en hexadecimal. Lo codificamos en utf-8 gracias a la función .encode(). 
            .apply(lambda hash_object: hash_object.hexdigest())
            # El hash object obtenido anteriormente lo conventimos en un numero hexadecimal 

)

df['uid'] = uids  # Añadimos el hash generado al dataframe
df.set_index('uid', inplace=True) # Ahora queremos que esta sea nuestro indice.

#print(df)

# Eliminamos los saltos de línea de nuestros ariculos contenidos en la columna body

stripped_body = (df
                    .apply(lambda row: row['body'], axis=1)
                    # Aplicamos una modificacion a cada una de las filas. La forma de obtener estas filas es diciendo que el axis=1
                    .apply(lambda body: list(body))  # Seleccionamos la columna body y convertimos cada fila en una lista de letras.
                    .apply(lambda letters: list(map(lambda letters: letters.replace('\n', ''), letters))) 
                    # Por cada letra en la lista de una fila del body reemplazamos en esta los saltos de lineas por espacios.
                    # Esto lo convertimos en un map para que podamos pasarle la lista con la que trabajará.
                    # Convertimos el objeto map entregado por la funcion map en un objeto lista.
                    .apply(lambda letters: ''.join(letters))
                    # Unimos las letras de cada lista para que obtener finalmente un string por fila

                )
print(stripped_body)