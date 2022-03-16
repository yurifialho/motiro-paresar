from curses.ascii import FS
import time
from tkinter.messagebox import RETRY
from spade.behaviour import FSMBehaviour, State
from app.util.logger import Logger
from app.config.config import Config

class NormalOperationBehav(FSMBehaviour):

    CHECK_CONNECTION = 'CHECK_CONNECTION'
    REGISTER = 'REGISTER'
    RESPONT_TO_MONITOR = 'RESPONT_TO_MONITOR'
    UPDATE_CONN_STATE = 'UPDATE_CONN_STATE'

    async def on_start(self) -> None:
        Logger.info('Setup Normal Operation Behaviour')
        return await super().on_start()

    async def on_end(self) -> None:
        Logger.info('Tear Down Normal Operation Behaviour')
        return await super().on_end()
    
    def preparePresence(self):
        self.presence.on_avaliable = self.on_avaliable
        self.presence.on_unavailable = self.on_unavailable
        self.presence.on_subscribed = self.on_subscribed
        self.presence.set_available()
        self.presence.approve_all = True

    def on_avaliable(self, jid : str, stanza) -> None:
        avaliables = self.get(Config.KN_TUIXAUA_ONLINE)
        if avaliables is None:
            avaliables = [jid]
        elif not jid in avaliables:
            avaliables.append(jid)
        Logger.info(f"Tuixaua [{jid}] - online")
        Logger.info(f"Has {len(avaliables)} Tuixaua online.")

    def on_unavailable(self, jid : str, stanza) -> None:
        avaliables = self.get(Config.KN_TUIXAUA_ONLINE)
        if not avaliables is None:
            Logger.info(f"Tuixaua [{jid}] - disconnected")
            avaliables.remove(jid)
            tuixauxaSeted = self.get(Config.KN_TUIXAUA_SETED)
            if jid == tuixauxaSeted and len(avaliables) > 0:
                self.set(Config.KN_TUIXAUA_SETED, avaliables[0])
            elif jid == tuixauxaSeted and len(avaliables) <= 0:
                self.set(Config.KN_TUIXAUA_SETED, None)
            Logger.info(f"Has {len(avaliables)} Tuixaua online.")

    def on_subscribed(self, jid : str) -> None:
        tuixauxaSeted = self.get(Config.KN_TUIXAUA_SETED)
        if tuixauxaSeted is None:
            Logger.info(f"Setting default tuixaua: {jid}")
            self.set(Config.KN_TUIXAUA_SETED, jid)
        Logger.info(f"Contact List: {self.presence.get_contacts()}")

    def setupTransitions(self) -> None:
        self.add_state(name=self.CHECK_CONNECTION, 
                       state=self.CheckConnectionState(), 
                       initial=True)
        self.add_state(name=self.REGISTER,
                       state=self.RegisterState())
        self.add_state(name=self.RESPONT_TO_MONITOR,
                       state=self.RespondToMonitorState())
        self.add_transition(source=self.CHECK_CONNECTION, dest=self.REGISTER)
        self.add_transition(source=self.REGISTER, dest=self.RESPONT_TO_MONITOR)
        self.add_transition(source=self.RESPONT_TO_MONITOR, dest=self.CHECK_CONNECTION)

    class CheckConnectionState(State):

        async def run(self) -> None:
            self.agent.normaloperationbehav.preparePresence()
            withoutConn = True
            while(withoutConn):
                Logger.info('Checking connection with any Tuixaua Agent')
                self.agent.retainCorrectContacts()
                tuixauaSetted = self.agent.get(Config.KN_TUIXAUA_SETED)
                if tuixauaSetted is None or tuixauaSetted == "":
                    Logger.error("No Tuixaua agent is available!")
                    time.sleep(5)
                else:
                    break
            self.set_next_state(NormalOperationBehav.REGISTER)

    class RegisterState(State):

        async def run(self) -> None:
            Logger.info('Process Request')
            time.sleep(5)
            self.set_next_state(NormalOperationBehav.RESPONT_TO_MONITOR)
    
    class RespondToMonitorState(State):
        
        async def run(self) -> None:
            Logger.info('Check if tuixaua is online')
            isOnline = True
            while(isOnline):
                tuixauaSetted = self.agent.get(Config.KN_TUIXAUA_SETED)
                if tuixauaSetted is None or tuixauaSetted == "":
                    isOnline = False
                    break
                else:
                    time.sleep(10)
            self.set_next_state(NormalOperationBehav.CHECK_CONNECTION)

 
