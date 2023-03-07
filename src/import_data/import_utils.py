'''MODULO PER FUNZIONI BASE SU DATI IMPORTATI'''

import logging
import pandas as pd
import os

logger = logging.getLogger('root')

def check_path(path: str) -> bool:
    '''Controllo se il path esiste'''
    if os.path.isdir(path) == False:
        raise FileNotFoundError (f"Percorso non trovato:\n {path}")

def importa_excel_as_df(path: str, file_name: str, sheet_name: str) -> pd.DataFrame:
    '''Importa file excel come dataframe'''
    check_path(path)
    file = os.path.join(path, file_name)
    df = pd.read_excel(file, sheet_name = sheet_name)
    return df

def filtra_colonne_df(df: pd.DataFrame , lista_col : list) -> pd.DataFrame:
    '''Tengo solo le colone specificate in lista_col nel DataFrame in input'''
    try:
         df_filt =  df[lista_col]
    
    except KeyError:
        logger.error("Verificare nomi colonne file input")
        raise KeyError
    
    return df_filt