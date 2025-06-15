from telethon import events
import datetime
import re
from config import rand,fileN

from FileWork import write_counter


async def ResultLog(client, chat_id):
    ResultSave(client, chat_id)
    ResultNum(client, chat_id)
    
    
#Функция сохранения результатов
def result_log(file_name, numR, colorR, numberR, hetR, timeR):
    with open(file_name, 'a', encoding='utf-8') as save:
        line = f'Раунд {numR} - Время: {timeR} - Цвет: {colorR} - Число: {numberR} - Чет: {hetR}\n'
        save.write(line)
        
#Обработка результатов
def ResultSave(client, chat_id):
    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        global rand, fileN
        text = event.raw_text.strip()

        match = re.match(r'Рулетка:\s*(\d{1,2}|3[0-6]|36)([🔴⚫🟢])', text)
        if match:
            number = match.group(1)
            color = match.group(2)

            timeR = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            het = 1 if int(number) % 2 == 0 else 0
            rand += 1
            write_counter(rand)

            await event.reply(
                f'Сохранено:\nРаунд {rand}\nВремя: {timeR}\nЦвет: {color}\nЧисло: {number}\nЧет: {het}'
            )
    
            result_log(fileN, rand, color, number, het, timeR)

#Показ номера раунда
def ResultNum(client, chat_id):
    @client.on(events.NewMessage(chats=chat_id))
    async def Nomrr(event):
        if event.text == 'Номер':
            await event.edit(f"Номер раунда {rand}")


#Функция пометки !ПОКА НЕ ИСПОЛЬЗУЕТСЯ!
def marks_log(file_name, rand):
    with open(file_name, 'a', encoding='utf-8') as save:
        save.write(rand)