''' MODULO MAIN PRINCIPALE'''

import log
import os
from import_data import da_server



def main():
    cr_server_path = r'\\UDI4FS01.EMEA.BOSCH.COM\Report_freud$\OAP_CSB'
    cr_input_file = 'OAP_CSB.xlsx'
    cr_output_file = 'items.xlsx'

    path_input_elaborati = os.path.realpath(os.path.join(os.path.dirname(__file__), '../', 'input/input_elaborati'))
    uso_leveling = False

    logger = log.setup_custom_logger('root')
    logger.debug('main message')
    da_server.cartelle_rosse(uso_leveling, cr_server_path, cr_input_file, cr_output_file, path_input_elaborati)

    pass


if __name__ == "__main__":
    main()