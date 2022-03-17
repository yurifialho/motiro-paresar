from spade.agent import Agent
from app.behavihours.normaloperationbehav import NormalOperationBehav
from app.behavihours.connectionmonitorbehav import ConnectionMonitorBehav
from app.config.config import Config
from app.util.logger import Logger

class ParesarAgent(Agent):
    
    def __init__(self, jid: str, password: str, verify_security: bool = False):
        self.normaloperationbehav = None
        self.connectionmonitorbehav = None
        super().__init__(jid, password, verify_security)

    async def setup(self):
        self.connectionmonitorbehav = ConnectionMonitorBehav()
        self.add_behaviour(self.connectionmonitorbehav)

        #self.normaloperationbehav = NormalOperationBehav()
        #self.normaloperationbehav.setupTransitions()
        #self.add_behaviour(self.normaloperationbehav)
        #b = self.Behav2()
        #self.add_behaviour(b)