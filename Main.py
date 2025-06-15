from telethon import TelegramClient
from AvtoPlay import AvtoPlay
from ResultLog import ResultLog
from config import AVAILABLE_CHATS, api_id,api_hash
import time

from OtherCommands import OtherCommands
from PredictionManager import PredictionManagerSetup

print("Доступные чаты:")
for num, (name, _) in AVAILABLE_CHATS.items():
    print(f"{num}. {name}")

while True:
    try:
        choice = int(input("Выберите номер чата: "))
        if choice in AVAILABLE_CHATS:
            chat_id = AVAILABLE_CHATS[choice][1]
            print(f"Выбран чат: {AVAILABLE_CHATS[choice][0]}")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
    except ValueError:
        print("Пожалуйста, введите число.")

client = TelegramClient('session_name', api_id, api_hash)


async def main():
    await ResultLog(client, chat_id)
    await AvtoPlay(client, chat_id)
    await OtherCommands(client,chat_id)
    await PredictionManagerSetup(client,chat_id)
    #Уведомление


while True:
    try:
        client.start()
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 10 сек...")
        time.sleep(10)