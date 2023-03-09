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

def merge_df(df: pd.DataFrame, df2: pd.DataFrame, col: str) -> pd.DataFrame:
    '''Unisco 2 dataframe in base ai valori della colonna col'''

    df_merged = df.merge(df2, left_on = col, right_on = col)
    check_missing_data(df, df_merged, col)
    return df_merged

def check_missing_data(df: pd.DataFrame, df_merged: pd.DataFrame, col: str) -> None:
    '''Controllo se durante la fase di merge perdo dei dati rispetto al df 
    originale'''

    if df.shape[0] > df_merged.shape[0]:
        logger.warning(f"Alcuni dati non possono essere trovati: {col} ")
        codes_pre_merge= set(df[col].squeeze())
        codes_post_merge = set(df_merged[col].squeeze())
        logger.warning(f"Codici mancanti:{codes_pre_merge.symmetric_difference(codes_post_merge)}")