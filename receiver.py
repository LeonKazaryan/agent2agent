import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class ReceiverAgent(Agent):
    class ReceiveNumber(CyclicBehaviour):
        async def on_start(self):
            self.numbers = []

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                number = int(msg.body)
                print(f"Агент 2 получил число: {number}")
                self.numbers.append(number)

                # Считаем среднее
                if len(self.numbers) > 0:
                    average = sum(self.numbers) / len(self.numbers)
                    print(f"Среднее значение: {average}")

                    # Даём рекомендацию
                    recommendation = "побольше" if average < 5 else "поменьше"
                    reply = Message(to=str(msg.sender))
                    reply.body = recommendation
                    await self.send(reply)
                    print(f"Агент 2 отправил рекомендацию: {recommendation}")
            else:
                print("Агент 2 не получил число за 10 секунд")

    async def setup(self):
        print("Агент 2 запущен")
        b = self.ReceiveNumber()
        self.add_behaviour(b)  

async def main():
    agent = ReceiverAgent("receiver@jabber.hot-chilli.net", "password")
    await agent.start()
    await asyncio.sleep(15)  
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())