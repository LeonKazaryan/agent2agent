import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import asyncio

class ReceiverAgent(Agent):
    class ReceiveMessage(OneShotBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Исправлено: self.receive вместо self.agent.receive
            if msg:
                print(f"Агент 2 получил сообщение: {msg.body}")
                reply = Message(to=str(msg.sender))  # Отправляем ответ
                reply.body = "Привет, я получил твое сообщение!"
                await self.send(reply)
                print("Агент 2 отправил ответ: Привет, я получил твое сообщение!")
            else:
                print("Агент 2 не получил сообщение за 10 секунд")

    async def setup(self):
        print("Агент 2 запущен")
        b = self.ReceiveMessage()
        self.add_behaviour(b)

async def main():
    agent = ReceiverAgent("receiver@jabber.hot-chilli.net", "password")
    await agent.start()
    await asyncio.sleep(10)  # Даём агенту 10 секунд на выполнение
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())