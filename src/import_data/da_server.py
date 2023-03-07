'''MODULO PER IMPORTARE DATI DA SERVER/QUERY'''

import logging
import os
import re
import shutil
from typing import Dict
from import_data import import_utils as iu


logger = logging.getLogger('root')


def copia_OAP_da_server(cr_server_path: str, cr_input_file: str, path_input_elaborati: str, estensione = ".xlsx") -> None:
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


def cartelle_rosse(uso_leveling: bool, cr_server_path: str, cr_input_file: str,
                   cr_output_file: str, path_input_elaborati: str) -> None:
    '''Importo da file su server cartelle rosse filtrandolo e salvandolo su
    input_elaborati'''

    lista_col = ['PO','Item','Class_n8', 'Class_n4', 'Wh', 'Promise_date','WKCenter',
                 'Stage_status', 'WkCenter_date', 'Spurs', 'OpenQty', 'POrder_next_stage']


    #Cerco sul server l'ultima versione di OAP_CSB e la copio su input\input_elaborati.
    copia_OAP_da_server(cr_server_path, cr_input_file, path_input_elaborati, estensione = ".xlsx")

    #Importo df da excel
    #df_cr = iu.import_excel_as_df(path, nome_input, sheet_name = "Sheet 1")

    
    logger.debug('submodule message')


