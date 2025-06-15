
import asyncio
from telethon import events
from config import AVTO,active_task


async def AvtoPlay(client, chat_id):
    StartAvtoPlay(client, chat_id)
    

#Функция автоигры
async def betting_loop(client,chat_id):
    global AVTO
    while not AVTO:
        try:
            await client.send_message(chat_id, '1 к')
            print("Ожидаю: Ставка принята...")
            async with client.conversation(chat_id) as conv:
                response = await conv.wait_event(
                    events.NewMessage(
                        func=lambda e: 'ставка принята' in e.text.lower()))

            await client.send_message(chat_id, 'Жду 15 сек')
            await asyncio.sleep(20)
            await client.send_message(chat_id, 'Го')
            await asyncio.sleep(10)
        except Exception as e:
            if AVTO:
                break
            
            
#Запуск автоигры
def StartAvtoPlay(client, chat_id):
    @client.on(events.NewMessage(chats=chat_id))
    async def gogg(event):
        global AVTO, active_task
        if event.text == 'АвтоС':
            AVTO = True
            if active_task:
                active_task.cancel()
            await client.send_message(event.chat_id, 'Останавливаю цикл')

        elif event.text == 'Авто' and not AVTO:
            if active_task and not active_task.done():
                await event.respond('Уже запущен')

            AVTO = False
            await client.send_message(event.chat_id, 'Запуск цикла')
            await asyncio.sleep(1)
            active_task = asyncio.create_task(betting_loop(event.chat_id))