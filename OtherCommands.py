from telethon import events


async def OtherCommands(client,chat_id):
    PingPong(client,chat_id)
    ID_Chat(client)
    


#Пинг-понг проверка
def PingPong(client,chat_id):
    @client.on(events.NewMessage(chats=chat_id))
    async def ping(event):
        if event.text == 'Пинг':
            await event.reply('Понг')
        
#Айди !ОТКЛЮЧЕНО!
def ID_Chat(client):
    @client.on(events.NewMessage)
    async def get_chat_id(event):
        return  #ОТКЛЮЧЕНО

        sender = await event.get_sender()
        print(f"Chat ID: {event.chat_id}")
        print(f"Sender ID: {sender.id}")
        print(f"Message text: {event.raw_text}")