import time

from spade.behaviour import OneShotBehaviour
from aioxmpp.stanza import Presence

from app.util.logger import Logger
from app.config.config import Config


class ConnectionMonitorBehav(OneShotBehaviour):

    # --- METHODS OVERRIED ---

    async def on_start(self) -> None:
        Logger.info('Setup Normal Operation Behaviour')
        return await super().on_start()
    
    async def on_end(self) -> None:
        Logger.info('Tear Down Normal Operation Behaviour')
        self.presence.set_unavailable()
        return await super().on_end()

    async def run(self) -> None:
        self.prepare_presence()
        self.retain_correct_contacts()
        while(True):            
            time.sleep(5)
    
    # ---------------------------

    def prepare_presence(self) -> None:
        self.presence.on_avaliable = self.on_avaliable
        self.presence.on_unavailable = self.on_unavailable
        self.presence.on_subscribed = self.on_subscribed
        self.presence.on_subscribe = self.on_subscribe
        self.presence.set_available()
        Logger.info("ConnectionMonitorBehav was prepared")

    def retain_correct_contacts(self):
        Logger.info("Checking contats connections...")
        
        listAgents = Config.getTuixauaAgents()
        Logger.info(f"Tuixauas to connect [{listAgents}]")
        contatos = []
        for jidx in self.presence.get_contacts().keys():
            contatos.append(f"{jidx.localpart}@{jidx.domain}")
        Logger.info(f"Retain Aready Contact List: {contatos}")
        if not contatos is None:
            subs = set(listAgents)-set(contatos)
            Logger.info(f"To Connects [{subs}]")
            for sub in subs:
                Logger.info(f"Registring to tuixaua connection [{sub}]")
                self.presence.subscribe(sub)
            unsubs = set(contatos)-set(listAgents)
            Logger.info(f"To Disconnects [{subs}]")
            for unsub in unsubs:
                Logger.info(f"Unregistring to tuixaua connection [{sub}]")
                self.presence.unsubscribe(unsub)
        Logger.info("Contats are ok!")

    def on_avaliable(self, jid : str, stanza : Presence) -> None:
        Logger.info(f"Tuixaua [{jid}] - online")
        avaliables = self.get(Config.KN_TUIXAUA_ONLINE)
        if avaliables is None:
            avaliables = [jid]
        elif not jid in avaliables:
            avaliables.append(jid)        
        Logger.info(f"Has {len(avaliables)} Tuixaua online.")

    def on_unavailable(self, jid : str, stanza : Presence) -> None:
        Logger.info(f"Tuixaua [{jid}] - disconnected")
        avaliables = self.get(Config.KN_TUIXAUA_ONLINE)
        if not avaliables is None:
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

    def on_subscribe(self, jid : str) -> None:
        Logger.info(f"Tuixaua [{jid}] asked for subscription.")
        self.presence.aprove(jid)
        Logger.info(f"Tuixaua [{jid}] subscription aproved .")