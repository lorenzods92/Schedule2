'''MODULO GENERALE IMPORT DI DATI INPUT, CONTIENE
- IMPORT ITEMS (carica_input_items_main) 
- IMPORTA ARTICOLI IN MACCHINA (carica_input_items_in_macchina)
- IMPORTA DB LAME ( E LEGENDA COME DIZ.)
OBIETTIVO MODULO: CREARE TUTTI I FILE EXCEL INPUT PER IL PROGRAMMA'''

import os
import logging
from import_data import items_input, query_input, dati_lama_input
from import_data import import_utils as iu

logger = logging.getLogger('root')


def carica_input_items(path_input_elab: str, path_input: str, uso_leveling: bool,
                            importa_cartelle_rosse_da_server: bool) -> None:
    '''Importo/carico i file excel che saranno l'input per il programma items.xlsx'''
    
    #Dati input items (cartelle rosse).
    cr_server_path = r'\\UDI4FS01.EMEA.BOSCH.COM\Report_freud$\OAP_CSB'
    cr_input_file = 'OAP_CSB.xlsx'
    cr_output_file = 'items.xlsx'
    importa_cartelle_rosse_da_server = True

    #Creo items.xlsx.
    items_input.crea_input_items(path_input_elab, path_input, uso_leveling, cr_server_path,
                                cr_input_file, cr_output_file,
                                importa_cartelle_rosse_da_server)

def carica_input_items_in_macchina(path_input_elab: str, path_input: str, gruppi_attivi: list) -> None:
    '''Creo file excel items_in_machine.xlsx input per articoli in macchina'''

    #Dati articoli in macchina / query.
    file_macc = "machines.xlsx"
    file_query = "query1.xlsx"
    nome_output = "items_in_machines.xlsx"

    #Update query articoli in macchina.
    file = os.path.join(path_input, file_query)
    query_input.update_query(file)

    #Import df query.
    df_query = query_input.importa_df_query_items(path_input, file_query, gruppi_attivi)
    
    #Importo df macc.
    df_macc_query = query_input.importa_df_macc_per_query(path_input,
                                                         file_macc, gruppi_attivi)

    #Unisco df macc e query per avere i dati items in macc.
    df_items_in_macc = iu.merge_df(df_macc_query, df_query, col = "CESPITE")
    
    #Salvo df su excel.
    df_items_in_macc.to_excel(os.path.join(path_input_elab, nome_output), sheet_name='Sheet1') 
    
    logger.info(f"Importati {len(df_items_in_macc)} articoli da query, gruppi attivi = {gruppi_attivi}")

def carica_database_lame(path_input: str, path_input_elab: str) -> None:
    '''Importo database LC dati lama e la legenda'''
    #Dati DB Lame.
    path_output = path_input_elab
    nome_input = "LC_DATI_LAMA.xlsx"
    nome_output = 'LC_Dati.xlsx'

    #Importo df LC_DATI_LAMA.
    #Mettere a posto AttributeError: 'NoneType' object has no attribute 'to_excel'
    df_dati_lama = dati_lama_input.importa_LC_db(path_input, path_output, nome_input)

    #Salvo df su excel.
    df_dati_lama.to_excel(os.path.join(path_output, nome_output), sheet_name='Sheet1') 
    
    logger.info(f"Importati {len(df_dati_lama)} articoli da cartelle LC_DATI")