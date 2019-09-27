import logging

class LoggerService:
    def __init__(self, debug):
        self.__debug = debug

    def writeDebug(self, message):
        if(self.__debug):
            logging.info(message)