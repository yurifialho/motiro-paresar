from spade.agent import Agent
from app.behavihours.normaloperationbehav import NormalOperationBehav
from app.config.config import Config
from app.util.logger import Logger

from spade.behaviour import OneShotBehaviour

class ParesarAgent(Agent):

    normaloperationbehav = None

    async def setup(self):
        self.normaloperationbehav = NormalOperationBehav()
        self.normaloperationbehav.setupTransitions()
        #self.add_behaviour(self.normaloperationbehav)
        b = self.Behav2()
        self.add_behaviour(b)

    def retainCorrectContacts(self):
        Logger.info("Checking contats connections...")
        listAgents = Config.getTuixauaAgents()
        contatos = self.normaloperationbehav.presence.get_contacts()
        Logger.info(f"Retain Contact List: {self.normaloperationbehav.presence.get_contacts()}")
        if not contatos is None:
            for sub in (set(listAgents)-set(contatos)):
                Logger.info(f"Registring to tuixaua connection [{sub}]")
                self.normaloperationbehav.presence.subscribe(sub)
            for unsub in (set(contatos)-set(listAgents)):
                Logger.info(f"Unregistring to tuixaua connection [{sub}]")
                self.normaloperationbehav.presence.unsubscribe(unsub)
        Logger.info("Contats are ok!")

    class Behav2(OneShotBehaviour):
        def on_available(self, jid, stanza):
            Logger.info("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))

        def on_subscribed(self, jid):
            Logger.info("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
            Logger.info("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            Logger.info("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            self.presence.set_available()
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available
            Logger.info("Teste1")
            self.presence.subscribe(Config.getXMPPUser())
            Logger.info("Teste2")
