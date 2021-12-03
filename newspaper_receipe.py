import argparse
#from typing_extensions import ParamSpec
import pandas as pd
from urllib.parse import urlparse
import hashlib
import nltk
from nltk.corpus import stopwords


import logging
#parametrizamos las variables de logging para que muestre los archivos a nivel INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Iniciando la limpieza de datos...')
#Crear DataFile para recibir los datos del archivo
    df = _read_data(filename)
    #Extraer el nombre de la primera parte del nombre del archivo = 'eluniversal'
    newspaper_uid = _extract_uid(filename)
    #Incluir la parte del nombre del archivo como columna
    df = _add_column_uid(df, newspaper_uid)
    #Extraer los hosts de la columna url
    df = _extract_host(df)
    #Reemplazar datos faltantes (Nan) de la columna title, utilizando los ultimos datos de la url
    df = _replace_missing_titles(df)
    #Limpiar datos creando un id único 
    df = _generate_uid(df)
    #quitando saltos de línea limpieza_datos.py
    df = _remove_lines(df)
    #tokenizar columna title = darle peso a las palabras
    df = _tokenize_column(df, 'title')
    #tokenizar columna body = darle peso a las palabras
    df = _tokenize_column(df, 'body')
    #Remover duplicados
    df = _remove_duplicates(df, 'title')
    #limpiar valores faltantes
    df = _drop_rows_with_missing_values(df)
    #salvar archivo en disco
    _save_data(df, filename)
    
    
    return df
    

def _read_data(filename):
    logger.info('Leyendo el archivo..{}'.format(filename))
    return pd.read_csv(filename)


def _extract_uid(filename):
    logger.info('Extrayendo primera parte del nombre del archivo...')
    newspaper_uid = filename.split('_')[0]
    logger.info('Se extrajo el nombre: {}'.format(newspaper_uid))
    return newspaper_uid


def _add_column_uid(df, newspaper_uid):
    logger.info('Incluyendo columna newspapper con el valor {}'.format(newspaper_uid))
    df['newspaper'] = newspaper_uid
    return df


def _extract_host(df):
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df


def _replace_missing_titles(df):
    logger.info('Reemplazando datos Nan del título')
    mask = df['title'].isna()
    missing_titles = (df[mask]['url']
            .str.extract(r'(?P<missing_titles>[^/]+)$')
            .applymap(lambda title: title.split('_'))
            .applymap(lambda title: ' '.join(title))
         )

    df.loc[mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    return df


def _generate_uid(df):
    logger.info('Generando UID únicos com md5')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis = 1)
            .apply(lambda hash_object: hash_object.hexdigest())
           )
    df['uid'] = uids

    return df.set_index('uid')

def _remove_lines(df):
    logger.info('Removiendo saltos de línea')

    #También se puede lograr con una línea de código
    #df.apply(lambda row: row['body'].replace('\n', ''), axis=1)

    stripped_body = (df
                    .apply(lambda row: row['body'], axis=1)
                    .apply(lambda body: list(body))
                    .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)))
                    .apply(lambda letters: ''.join(letters))
    )

    df['body'] = stripped_body
    return df


def _tokenize_column(df, column_name):
    logger.info('Calculating the number of unique tokens in {}'.format(column_name))
    stop_words = set(stopwords.words('spanish'))

    n_tokens =  (df
                 .dropna()
                 .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                 .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                 .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                 .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                 .apply(lambda valid_word_list: len(valid_word_list))
            )

    df['n_tokens_' + column_name] = n_tokens

    return df


def _remove_duplicates(df, column_name):
    logger.info('Removiendo duplicados de la columna{}'.format(column_name))
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df


def _drop_rows_with_missing_values(df):
    logger.info('Eliminando registros donde no hay valores')
    return df.dropna()


def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Salvando archivo limpio')
    df.to_csv(clean_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Describir el path que se le hará limpieza de datos',
                        type=str)

    arg = parser.parse_args()

    df = main(arg.filename)
    print(df)
