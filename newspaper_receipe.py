import argparse
#from typing_extensions import ParamSpec
import pandas as pd
from urllib.parse import urlparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Describir el path que se le hará limpieza de datos',
                        type=str)

    arg = parser.parse_args()

    df = main(arg.filename)
    print(df)
