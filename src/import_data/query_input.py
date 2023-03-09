'''MODULO PER CREARE DATI DI INPUT PROGRAMMA SU QUERY ARTICOLI IN MACCHINA:
- FUNZIONI PER AGGIORNARE QUERY
- FUNZIONI PER IMPORTARE DATI MACCHINE
OBIETTIVO MODULO: CREARE FILE items_in_machine.xlsx INPUT PER IL PROGRAMMA'''

import logging
import win32com.client
import numpy as np
import pandas as pd
from import_data import import_utils as iu

logger = logging.getLogger('root')


def importa_df_query_items(path_input: str, file_query: str, 
                            gruppi_attivi: list) -> pd.DataFrame:
    '''Estraggo df_query da file excel query'''

    #Importo la query
    df_query = iu.importa_excel_as_df(path_input, file_query, sheet_name = "Query1")

    #tengo solo le colonne necesarie a items in macc.
    lista_col_query = ['CODCDL','DESCDL','AREA', 'STATUS', 'DESFASE', 
                       'ITEM', 'CODORDINE', 'LOTTO', 'QTAPROD',
                       'PREVIOUS_ITEM', 'PREVIOUS_ORDER']
    df_query = iu.filtra_colonne_df(df_query, lista_col_query)
    
    #Rinomino colonne in modo da non crare conflitti nel merge.
    df_query = df_query.rename(columns={"CODCDL": "CESPITE",
                                        "ITEM": "CODICE",
                                        "STATUS": "SITUAZIONE",
                                        "CODORDINE" : "PO"})

    #filtro le macchine che voglio usare, codifica query.
    if 'SISTECH' in gruppi_attivi: gruppi_attivi.append('DFS')
    if 'CHF210' in gruppi_attivi: gruppi_attivi.append('CHF')
    
    df_query = df_query[df_query.AREA.isin(gruppi_attivi)]
    
    #calcolo lotto rimanente.
    df_query = calcola_lotto_rimanente(df_query)
    
    #tolgo i codici fittizzi e li sostituisco con quelli precedenti.
    df_query['LOTTO'] = np.where(df_query['CODICE'] != 'FITTIZIO', df_query['LOTTO'], 0)
    df_query['CODICE'] = np.where(df_query['CODICE'] != 'FITTIZIO', df_query['CODICE'], df_query['PREVIOUS_ITEM'])
    
    #aggiungo colonne numero, prio ( sempre zero) e status (sempre attiva).
    df_query['PRIO'] = 0
    df_query['STATUS'] = 'ATTIVA'
    df_query.insert(0, 'NUMERO', range(1000, 1000 + len(df_query)))

    return df_query

    
def importa_df_macc_per_query(path_input: str, file_macc: str,
                             gruppi_attivi: list) -> pd.DataFrame:

    #Importo dati macchina su df.
    df_macc = iu.importa_excel_as_df(path_input, file_macc, sheet_name = "Sheet1")

    #Tengo solo le colonne necessarie a items in macc.
    lista_col = ['GRUPPO','TIPO_MACCHINA','NOTE_MACCHINA', 'CESPITE', 'ISOLA', 
                 'DMIN', 'DMAX', 'TIPO_DIST', 'D_MANIP', 'DMIN_MANIP', 'DMAX_MANIP']
    df_macc = iu.filtra_colonne_df(df_macc, lista_col)

    #Rinomino colonne df_macc in modo da non crare conflitti nel merge.
    df_macc = df_macc.rename(columns={"GRUPPO": "M_GRUPPO",
                            "TIPO_MACCHINA": "M_TIPO_MACCHINA",
                            "ISOLA" : "M_ISOLA",
                            "DMIN" : "M_DMIN",
                            "DMAX" : "M_DMAX",
                            "TIPO_DIST" : "M_TIPO_DIST",
                            "D_MANIP" : "M_D_MANIP",
                            "DMIN_MANIP" : "M_DMIN_MANIP",
                            "DMAX_MANIP" : "M_DMAX_MANIP",})

    #Filtro le macchine che voglio usare, tengo solo quelle nella lista attive.
    df_macc = df_macc[df_macc.M_GRUPPO.isin(gruppi_attivi)]

    return df_macc


def update_query(file: str) -> None:
    '''Update query del file specificato in input'''
    
    xlapp = win32com.client.DispatchEx("Excel.Application")
    wb = xlapp.Workbooks.Open(file)
    wb.RefreshAll()
    xlapp.CalculateUntilAsyncQueriesDone()
    wb.Save()
    xlapp.Quit()


def calcola_lotto_rimanente(df_query: pd.DataFrame) -> pd.DataFrame:
    '''Trovo la quantità rimanente da lavorare'''
    df_query['LOTTO'] = df_query['LOTTO'] - df_query['QTAPROD']
    
    #pongo a zero se ho prodotto più del pianificato
    df_query['LOTTO'] = df_query['LOTTO'].mask(df_query['LOTTO'] < 0, 0)
    
    return df_query