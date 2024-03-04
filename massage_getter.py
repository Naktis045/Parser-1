
import asyncio
from telethon.sync import TelegramClient, events
from pars_conf import account, list_all, key_words # импортируем данные из файла конфигурации

api_id = account[0]  # задаем API
api_hash = account[1]  # задаем HASH
key_word = key_words[0]
channel_id = account[0]
print(account)


class KeyWordError(Exception):
    print("KeyWordError : key word not found")


client = TelegramClient('my_account', account[0], account[1])  # собираем телеграм клиента


@client.on(events.NewMessage) # обработчик который запускаеться при получении нового сообщения
async def my_event_handler(event,delay=86400):
    print("started")
    if event.chat.username in list_all:  # проверяем пришло ли событие из канала который входит в наш список
        if len(key_words) != 0:
            for i in range(0, len(key_words)):
                if key_words[i] in event.message.message:
                    await client.forward_messages(account[2],
                                                  event.message)  # пересылаем сообщение в нашу личный канал
                    print("busted for key word")# выводим в консоль оповещение
                chat = await event.get_input_chat()  # получаем данные канала из которого пришло событие
                msg = await client.get_messages(chat.channel_id,limit=3)  # берем послденее сообщение на канале
                for message in msg:  # Check if the keyword is present
                    if key_word in message.photo:  # Save message to photo.txt
                        with open('photo.jpg',encoding="TIFF-S") as file: # encoding="utf-8"
                            file.write(message.photo)
                            file.write()
                            file.write(message.media.photo)
                        print("Message saved to photo.jpg")
                        await asyncio.sleep(delay)
                        await client.start()
                        continue
        else:
            raise KeyWordError()
        print()  # выводим в консоль оповещени


def shaya():
    """  """
    client.start()
    client.run_until_disconnected()


if __name__ == '__main__':

    shaya()

