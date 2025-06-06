import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random
import json
import time

class SenderAgent(Agent):
    class SendNumber(CyclicBehaviour):
        async def on_start(self):
            self.current_number = random.randint(1, 10)

        async def run(self):
            # Отправляем число в файл
            data = {"number": self.current_number, "to": "receiver"}
            with open("agent_exchange.json", "w") as f:
                json.dump(data, f)
            print(f"Агент 1 (SPADE) отправил число: {self.current_number}")

            # Ждём ответа с рекомендацией
            for _ in range(5):  # Пробуем 5 раз с интервалом 1 секунда
                try:
                    with open("agent_exchange.json", "r") as f:
                        reply = json.load(f)
                    if reply.get("to") == "sender" and "recommendation" in reply:
                        print(f"Агент 1 получил рекомендацию: {reply['recommendation']}")
                        if "побольше" in reply["recommendation"]:
                            self.current_number += 1
                        elif "поменьше" in reply["recommendation"]:
                            self.current_number -= 1
                        break
                except FileNotFoundError:
                    pass
                await asyncio.sleep(1)  # Задержка 1 секунда перед следующей попыткой

            await asyncio.sleep(2)  # Задержка перед следующей итерацией

    async def setup(self):
        print("Агент 1 (SPADE) запущен")
        b = self.SendNumber()
        self.add_behaviour(b)

async def main():
    agent = SenderAgent("sender@jabber.hot-chilli.net", "password")
    await agent.start()
    await asyncio.sleep(30)  # Увеличиваем время работы до 30 секунд
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())