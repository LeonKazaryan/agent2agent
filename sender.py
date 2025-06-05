import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random

class SenderAgent(Agent):
    class SendNumber(CyclicBehaviour):
        async def on_start(self):
            self.current_number = random.randint(1, 10)  # Начальное число

        async def run(self):
            # Отправляем число
            msg = Message(to="receiver@jabber.hot-chilli.net")
            msg.body = str(self.current_number)
            print(f"Агент 1 отправляет число: {self.current_number}")
            await self.send(msg)

            # Ждём ответа
            reply = await self.receive(timeout=10)
            if reply:
                print(f"Агент 1 получил рекомендацию: {reply.body}")
                # Корректируем число на основе рекомендации
                if "побольше" in reply.body:
                    self.current_number += 1
                elif "поменьше" in reply.body:
                    self.current_number -= 1
            await asyncio.sleep(2)  # Задержка перед следующей итерацией

    async def setup(self):
        print("Агент 1 запущен")
        b = self.SendNumber()
        self.add_behaviour(b)

async def main():
    agent = SenderAgent("sender@jabber.hot-chilli.net", "password")
    await agent.start()
    await asyncio.sleep(15)  # Даём агенту 15 секунд на работу
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())