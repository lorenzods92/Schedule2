'''MODULO PER INIZIALIZZARE IL LOGGER'''
import logging

def setup_custom_logger(name: str) -> logging.Logger:
    '''Definisco Handler e logger'''
    formatter = logging.Formatter(fmt='%(levelname)s - %(module)s - %(message)s - %(asctime)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')

    #Handler per print su console
    std_handler = logging.StreamHandler()
    std_handler.setLevel(logging.DEBUG)
    std_handler.setFormatter(formatter)

    #Handler per scrittura su file .log
    file_handler = logging.FileHandler('logs.log', mode = "w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    #Aggiungo Handler a logger
    logger.addHandler(std_handler)
    logger.addHandler(file_handler)
    
    return logger