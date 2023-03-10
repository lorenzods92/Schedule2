'''MODULO PER IMPORTARE DATI DATABASE LAMA:
- FUNZIONI PER IMPORTARE DB DATI LAMA
-  FUNZIONE PER IMPORTARE LEGENDA DATI LAMA ( USATA POI IN INIZ. ITEMS)
OBIETTIVO MODULO: CREARE FILE LC_dati.xlsx INPUT PER IL PROGRAMMA'''

import logging
import os
import pandas as pd
from import_data import import_utils as iu

logger = logging.getLogger('root')

def importa_LC_db(path_input: str,  path_output: str, nome_input: str) -> pd.DataFrame:
    '''Funzione per importare database LC_DATI e ricavare il file .xlsx'''
    
    #Importo DB LC su DataFrame
    df = iu.importa_excel_as_df(path_input, nome_input, sheet_name = "Foglio2")
    
    #Tengo solo alcune colonne.
    lista_col = ["CODICE","TIPO","QUAL","DIFO","DELA","NDEN","PASSO","HPLAC",
                 "SPCO","PFDE","NRAS","MORD","PFFIA", "TEFL"]
    df = iu.filtra_colonne_df(df, lista_col)

    return df

def import_legenda_LC(path_input: str) -> dict:
    '''Importo i fogli legenda dati lama specificati come df e li ritorno come dict'''
    
    file_name = "Legenda_LC_DATI_LAMA"
    sheet_names = ["RIVESTIMENTO (TEFL)"]

    d_leg = {} 
    
    #Estraggo dataframe da excel
    for sheet_name in sheet_names:
        d_leg[sheet_name] = iu.import_excel_as_df(path_input, file_name + ".xlsx", sheet_name = sheet_name)
        
    return d_leg
    