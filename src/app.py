''' MODULO MAIN PRINCIPALE'''

import log
import os

from import_data import crea_input_excel


def main():
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    logger = log.setup_custom_logger('root')
    logger.debug('main message')

    #Dati generali.
    path_input_elab = os.path.realpath(os.path.join(os.path.dirname(__file__), '../', 'input/input_elaborati'))
    path_input = os.path.realpath(os.path.join(os.path.dirname(__file__), '../', 'input'))
    #Dati articoli.
    uso_leveling = False
    importa_cartelle_rosse_da_server = False
    #Dati query.
    gruppi_attivi = ['SISTECH','CHF270']
    
    #Creo excel di input
    crea_input_excel.carica_input_items(path_input_elab, path_input, uso_leveling, 
                                       importa_cartelle_rosse_da_server)

    crea_input_excel.carica_input_items_in_macchina(path_input_elab, path_input, gruppi_attivi)

    crea_input_excel.carica_database_lame(path_input, path_input_elab)
    
    
    pass


if __name__ == "__main__":
    main()