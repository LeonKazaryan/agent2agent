import asyncio
from autogen import AssistantAgent, UserProxyAgent
import random
import traceback

# Очереди для обмена сообщениями
send_queue = asyncio.Queue()
receive_queue = asyncio.Queue()

print("Инициализация очередей завершена")

# SenderAgent (без SPADE)
async def run_sender():
    try:
        print("SenderAgent запущен")
        current_number = random.randint(1, 10)
        print(f"Начальное число: {current_number}")

        while True:
            await send_queue.put({"number": current_number, "to": "receiver"})
            print(f"Агент 1 отправил число: {current_number}")

            try:
                reply = await asyncio.wait_for(receive_queue.get(), timeout=3)
                if reply.get("to") == "sender" and "recommendation" in reply:
                    print(f"Агент 1 получил рекомендацию: {reply['recommendation']}")
                    if "побольше" in reply["recommendation"]:
                        current_number += 1
                    elif "поменьше" in reply["recommendation"]:
                        current_number -= 1
                else:
                    print("Агент 1: Получен некорректный ответ:", reply)
            except asyncio.TimeoutError:
                print("Агент 1: Таймаут ожидания рекомендации")
            await asyncio.sleep(2)
    except Exception as e:
        print("Ошибка в run_sender:", e)
        traceback.print_exc()

# ReceiverAgent (AutoGen)
async def run_receiver():
    try:
        print("Инициализация ReceiverAgent")
        receiver = AssistantAgent(
            name="ReceiverAgent",
            system_message="Ты агент, который получает числа из send_queue, считает среднее и даёт рекомендацию ('побольше' или 'поменьше', если среднее < 5). Отправляй ответ в receive_queue."
        )
        user_proxy = UserProxyAgent(
            name="UserProxy",
            code_execution_config={"use_docker": False}
        )
        print("ReceiverAgent успешно создан")

        numbers = []
        while True:
            try:
                data = await asyncio.wait_for(send_queue.get(), timeout=2)
                if data.get("to") == "receiver" and "number" in data:
                    number = data["number"]
                    numbers.append(number)
                    average = sum(numbers) / len(numbers)
                    recommendation = "побольше" if average < 5 else "поменьше"
                    await receive_queue.put({"to": "sender", "recommendation": recommendation})
                    print(f"Агент 2 (AutoGen) получил число: {number}, среднее: {average}, рекомендация: {recommendation}")
            except asyncio.TimeoutError:
                print("Агент 2: Таймаут ожидания сообщения")
                await asyncio.sleep(1)
    except Exception as e:
        print("Ошибка в run_receiver:", e)
        traceback.print_exc()

# Запуск обоих агентов
async def main():
    try:
        print("Запуск SenderAgent")
        sender_task = asyncio.create_task(run_sender())

        print("Запуск ReceiverAgent")
        receiver_task = asyncio.create_task(run_receiver())

        await asyncio.sleep(30)

        print("Остановка агентов")
        sender_task.cancel()
        receiver_task.cancel()
    except Exception as e:
        print("Ошибка в main:", e)
        traceback.print_exc()

if __name__ == "__main__":
    print("Программа запущена")
    try:
        asyncio.run(main())
    except Exception as e:
        print("Ошибка в asyncio.run:", e)
        traceback.print_exc()
    print("Программа завершена")