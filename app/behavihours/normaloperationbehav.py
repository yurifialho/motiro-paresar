import time
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

    def setup_transitions(self) -> None:
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

 
