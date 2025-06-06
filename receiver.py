from autogen import AssistantAgent, UserProxyAgent
import json
import time

# Агент, который анализирует числа
receiver = AssistantAgent(
    name="ReceiverAgent",
    system_message="Ты агент, который получает числа из файла agent_exchange.json, считает среднее и даёт рекомендацию ('побольше' или 'поменьше', если среднее < 5). Записывай ответ в тот же файл."
)

# Прокси-агент для взаимодействия с файлом
user_proxy = UserProxyAgent(
    name="UserProxy",
    code_execution_config={"use_docker": False}
)

numbers = []  # список для хранения всех чисел

def read_and_process():
    global numbers
    while True:
        try:
            with open("agent_exchange.json", "r") as f:
                data = json.load(f)
            if data.get("to") == "receiver" and "number" in data:
                number = data["number"]
                numbers.append(number)  # сохранение числа
                average = sum(numbers) / len(numbers)
                recommendation = "побольше" if average < 5 else "поменьше"
                # выдача времени для чтения файла перед перезаписью
                time.sleep(0.5)
                reply = {"to": "sender", "recommendation": recommendation}
                with open("agent_exchange.json", "w") as f:
                    json.dump(reply, f)
                print(f"Агент 2 (AutoGen) получил число: {number}, среднее: {average}, рекомендация: {recommendation}")
        except FileNotFoundError:
            pass
        time.sleep(2)

# запуск обработки
if __name__ == "__main__":
    import threading
    threading.Thread(target=read_and_process, daemon=True).start()
    user_proxy.initiate_chat(receiver, message="Начни обработку")
    input("Нажми Enter для завершения...")