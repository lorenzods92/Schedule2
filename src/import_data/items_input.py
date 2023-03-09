'''MODULO PER CREARE DATI DI INPUT PROGRAMMA SU ITEMS'''

import logging
import os
import re
import shutil
import pandas as pd
from typing import Dict
from import_data import import_utils as iu


logger = logging.getLogger('root')


def crea_input_items(path_input_elab: str, path_input: str, uso_leveling: bool, 
                    cr_server_path:str, cr_input_file: str, cr_output_file: str, 
                    importa_cartelle_rosse_da_server: bool) -> None:
    ''' Salvo dati items su file excel items.xlsx (importando OAP e filtrando). Ci possono essere due situazioni:
    1) Importo i dati da server salvando OPA_CSB su path_input_elab ed estraendo i relativi dati
    2) Importo i dati da file OPA_CSB salvato su path_input (caso in cui voglia gestire il file manualmente)'''

    
    if importa_cartelle_rosse_da_server:
        #Creo file excel su input/input_elaborati da input server.
        cartelle_rosse(cr_server_path, cr_input_file, path_input_elab)
        #Creo DataFrame items dal file OAP_CSB estratto da server
        df_items = crea_df_items_da_cartelle_rosse(uso_leveling, path_input_elab,
                                                              cr_input_file)
    else:
        #Creo DataFrame items fa file OAP (gestione manuale).
        df_items = crea_df_items_da_cartelle_rosse(uso_leveling, path_input,
                                                              cr_input_file)
    #Salvo df su excel.
    df_items.to_excel(os.path.join(path_input_elab, cr_output_file), sheet_name = 'Sheet1')
    logger.debug(f'Creato file {cr_output_file}')


def crea_df_items_da_cartelle_rosse(uso_leveling: bool, cr_path_file: str, cr_input_file: str) -> pd.DataFrame:
    '''Creo dataframe da excel e lo filtro, il dataframe poi verrà salvato come .xlsx, in
    input viene chiesto:
    - uso_leveling: inserisco/escludo articoli leveling
    - cr_path_file: il percorso dove si trova il file [da server o salvato manualmente]
    - cr_input_file: il nome del file da filtrare [OAP_CSB.xlsx]
    - cr_output_file: il nome del file di output processato [items.xlsx]
    
    Filtro gli articoli tenendo i soli che:
    - sono in trasferimento affilatura [WK_center]
    - non sono in diamante
    - non sono in cromatura [stage stat == S]
    - non hanno i dentoni [Spurs == 0]
    - non sono campionature LCCAM'''

    #Importo df da excel OAP_CSB.
    df_cr = iu.importa_excel_as_df(cr_path_file, cr_input_file, sheet_name = "Sheet 1")

    #lista colonne da tenere.
    lista_col = ['PO','Item','Class_n8', 'Class_n4', 'Wh', 'Promise_date','WKCenter',
                 'Stage_status', 'WkCenter_date', 'Spurs', 'OpenQty', 'POrder_next_stage']
    #Filtro le colonne.
    df_cr = iu.filtra_colonne_df(df_cr, lista_col)

    
    wk_center = "TRASF. IN AFFILATURA"
    diamante = "420 884 AFFILATURA ESTERNA DENTI DIAMANTE"
    sigle_leveling = ['FL', 'DT', 'DL']

    df_cr_filt = df_cr[(df_cr['WKCenter'] == wk_center ) & (df_cr['POrder_next_stage'] != diamante) 
            & (df_cr['Stage_status'] == "S") & (df_cr['Spurs'] == 0) & ( 'LCCAM' not in df_cr['Item'])]

    #Tolgo i codici leveling se richiesto.
    if not uso_leveling:
        for sigla in sigle_leveling:
            df_cr_filt = df_cr_filt[(df_cr_filt['Class_n4'] != sigla)]

    #Aggiungo colonna prio.
    df_cr_filt['PRIO'] = 3
    
    #Rinomino colonne.
    df_cr_filt = df_cr_filt.rename(columns={"Item": "CODICE",
                            "Promise_date": "PROMISE_DATE",
                            "OpenQty" : "LOTTO"})
    
    #Rinomino la colonna index.
    df_cr_filt.index.names = ['NUMERO']

    return df_cr_filt

def copia_OAP_da_server(cr_server_path: str, cr_input_file: str, path_input_elaborati: str,
                        estensione = ".xlsx") -> None:
    '''Copia dal server il file OAP_CSB con la data più rencente e lo salva in input con il nome specificato'''

    NOME_FILE_SERVER = 'OAP_CSB_'
    PATTERN = 'OAP_CSB_[0-9]+'
    d_file: Dict[str, str] = {}

    #Seleziono solo i file con l'estensione specificata.
    lista_file= []
    for file in os.listdir(cr_server_path):
        if file.endswith(estensione):
            lista_file.append(file)

    lista = []
    #Seleziono la parte nel nome file che indica la data.
    for file in lista_file:
        pattern = re.compile(r'OAP_CSB_[0-9]+')
        match_data = pattern.finditer(file)

        for match in match_data:
            data_file = int(match.group(0).replace(NOME_FILE_SERVER, ''))
            #Salvo file e rispettiva data su dizionario.
            d_file[file] = data_file

    #trovo il file con la data più recente.
    source = max(d_file, key=d_file.get)
    target_folder = path_input_elaborati
    target_file = os.path.join(target_folder, cr_input_file)
    
    #copio e rinomino il file togliendo la parte di data.
    source_path_completo = os.path.join(cr_server_path, source)
    shutil.copy(source_path_completo, target_file)
    
    logger.info(f"Importati dati cartelle rosse da {source}")


def cartelle_rosse(cr_server_path: str, cr_input_file: str,
                   path_input_elaborati: str) -> None:
    '''Importo da file su server cartelle rosse filtrandolo e salvandolo su
    input_elaborati'''

    #Cerco sul server l'ultima versione di OAP_CSB e la copio su input\input_elaborati.
    copia_OAP_da_server(cr_server_path, cr_input_file, path_input_elaborati, estensione = ".xlsx")
 
