import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import asyncio

class SenderAgent(Agent):
    class SendMessage(OneShotBehaviour):
        async def run(self):
            msg = Message(to="receiver@jabber.hot-chilli.net")  # Адрес второго агента
            msg.body = "Привет!"
            print("Агент 1 отправляет сообщение: Привет!")
            await self.send(msg)  # Исправлено: self.send вместо self.agent.send

    async def setup(self):
        print("Агент 1 запущен")
        b = self.SendMessage()
        self.add_behaviour(b)

async def main():
    agent = SenderAgent("sender@jabber.hot-chilli.net", "password")
    await agent.start()
    await asyncio.sleep(5)  # Даём агенту 5 секунд на выполнение
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())