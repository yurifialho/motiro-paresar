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
            await asyncio.sleep(1)
    
    class InformBehav(OneShotBehaviour):
        async def run(self):
            logging.info("InformBehav running...")
            msg = Message(to="ruleragent@prosody-server")
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
        self.b = self.MyBehav()
        self.a = self.InformBehav()
        self.add_behaviour(self.b)
        self.add_behaviour(self.a)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # prosodyctl register planneragent prosody-server planneragent
    dummy = PlannerAgent("planneragent@prosody-server", "planneragent")
    future = dummy.start()
    future.result()

    logging.info("Wait until user interrupts with ctrl+C")
    while dummy.is_alive():
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping...")
            dummy.stop()
            break
    logging.info("Agent finished with exit code: {}".format(dummy.a.exit_code))