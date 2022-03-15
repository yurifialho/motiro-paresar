import time
import asyncio
import sys
import logging
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message

class PlannerAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            logging.info("Starting behaviour...")
            self.counter = 0

        async def run(self):
            logging.info("Counter: {}".format(self.counter))
            self.counter += 1
            logging.info("InformBehav running...")
            msg = Message(to="ruleragent@xmpp-server")
            msg.set_metadata("performative","inform")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language","OWL-S")
            msg.body = "Planner Hello"

            await self.send(msg)
            logging.info("Message sent")

            self.exit_code = "Msg sent finalized"
            await asyncio.sleep(5)
    
    class InformBehav(OneShotBehaviour):
        async def run(self):
            logging.info("InformBehav running...")
            msg = Message(to="ruleragent@xmpp-server")
            msg.set_metadata("performative","inform")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language","OWL-S")
            msg.body = "Planner Hello"

            await self.send(msg)
            logging.info("Message sent")

            self.exit_code = "Msg sent finalized"

            await self.agent.stop()


    async def setup(self):
        logging.info("Agent starting . . .")
        #self.b = self.MyBehav()
        #self.a = self.InformBehav()
        #self.add_behaviour(self.b)
        #self.add_behaviour(self.a)

async def get_controller(request):
    return {"number": 42}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # prosodyctl register planneragent prosody-server planneragent
    planneragent = PlannerAgent("motiro-paresar@xmpp-server", "motiro-paresar")
    planneragent.web.add_get('/info', get_controller, 'hello.html')
    future = planneragent.start(auto_register=True)
    #planneragent.web.start(hostname='planneragent', port="10002")
    # Template Engine: http://jinja.pocoo.org/docs/
    planneragent.web.start(hostname='planneragent', port="10002", templates_path="web/templates")
    future.result()

    logging.info("Wait until user interrupts with ctrl+C")
    while planneragent.is_alive():
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping...")
            planneragent.stop()
            break
    logging.info("Agent finished with exit code: {}".format(planneragent.a.exit_code))