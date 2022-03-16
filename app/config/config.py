import os
from posixpath import split
from xml import dom

from app.util.logger import Logger

class Config:
    """
        Classe responsável por retornar para as aplicação as
        configurações necessárias para execução

        @author: Yuri Fialho
        @since: 14/03/2022
    """

    AG_HOSTNAME = 'HOSTNAME'
    AG_PORT = 'PORT'
    AG_XMPP_USER = 'AG_XMPP_USER'
    AG_XMPP_PASS = 'AG_XMPP_PASS'
    AG_XMPP_HOST = 'AG_XMPP_HOST'

    DEBUG_MODE = 'DEBUG'
    WEB_ENABLED = 'WEB_ENABLED'

    AG_TUIXAUA_AGENTS = 'AG_TUIXAUA_AGENTS'

    KN_TUIXAUA_SETED = 'KN_TUIXAUA_SETED'
    KN_TUIXAUA_ONLINE = 'KN_TUIXAUA_ONLINE'

    @staticmethod
    def getEnvVariables(key : str) -> str :
        return os.getenv(key)

    @staticmethod
    def getXMPPUser(varuser : str = 'motiro-paresar', vardomain : str = 'localhost') -> str:
        envuser = Config.getEnvVariables(Config.AG_XMPP_USER)
        envhost = Config.getEnvVariables(Config.AG_XMPP_HOST)

        user = envuser if envuser else varuser
        domain = vardomain if vardomain != 'localhost' else envhost
        if domain is None:
            domain = vardomain

        if not user or not domain:
            raise Exception("User and domains is required to connect to XMPP Server!")
        else:
            return f"{user}@{domain}"
    
    @staticmethod
    def getXMPPPass(varpass : str = None) -> str:
        envpass = Config.getEnvVariables(Config.AG_XMPP_PASS)

        passwd = varpass if varpass else envpass

        if not passwd:
            return ''
        else:
            return passwd

    @staticmethod
    def isWebEnabled() -> bool:
        envweben = Config.getEnvVariables(Config.WEB_ENABLED)

        opts = ['false', 'n', 'nao', 'não', 'not', 'disabled']

        if not envweben:
            return True
        
        if envweben.lower() in opts:
            return False
        else:
            return True
    
    @staticmethod
    def getHostWebName(varhost : str = 'localhost') -> str:
        envhost  = Config.getEnvVariables(Config.AG_HOSTNAME)
        if envhost:
            return envhost
        else:
            return varhost

    @staticmethod
    def getHostWebPort(varport : str = '10001') -> str:
        envport  = Config.getEnvVariables(Config.AG_PORT)
        if envport:
            return envport
        else:
            return varport

    @staticmethod
    def getTuixauaAgents() -> list:

        strAgents = Config.getEnvVariables(Config.AG_TUIXAUA_AGENTS)
        Logger.info(f"Tuixaua Agentes to Connect={strAgents}")

        if strAgents == None or strAgents == '':
            raise Exception("You have indicate almost one chief agent (set AG_TUIXAUA_AGENT env)")

        return strAgents.split(',')