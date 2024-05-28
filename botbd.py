import time
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API
import sql_db

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def auth(func):
    async def wrapper(message):
        if message['from']['id'] != 723304467:
            return await message.reply("Access Denied", reply=False)
        elif message['from']['id'] != 723304467: # ID М.В.
            return await message.reply("Access Denied", reply=False)
        return await func(message)

    return wrapper

async def on_startup(_):
    await sql_db.db_connect()
    print('Подключение к бд успешно')

# async def send_reminders():
#     get_d = await sql_db.get_data()
#     for el in get_d:
#         a = f'<b>Дата окончания:</b> {el}'
#         await bot.send_message(chat_id=message.from_user.id, text=a, parse_mode='html')

# async def scheduled(wait_for):
#     while True:
#         await send_reminders()
#         await asyncio.sleep(wait_for)

# # Остальной код

# @dp.message_handler(commands=['start', 'help'])
# async def cmd_start(message: types.Message):
#     await bot.send_message(chat_id=message.from_user.id, 
#                            text='Бот для напоминания о приближающейся дате окончания срока действия ЭЦП')
        
#     asyncio.create_task(scheduled(604800))  # Один раз в неделю (в секундах)



@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    get_d = await sql_db.get_data()
    await bot.send_message(chat_id=message.from_user.id, 
                           text='Бот для напоминания о приближающейся дате окончания срока действия ЭЦП')
        
    for i in range(1): # кол-во недель в году       
        for el in get_d:
            a = f'<b> дата окончания: </b>'.join(el)
            try:
                await bot.send_message(chat_id=message.from_user.id, text=a, parse_mode='html')
            except exceptions.TelegramAPIError as e:
                print(f"An error occurred while sending message: {str(e)}")
        time.sleep(604800)
        
    # for i in range(55): # кол-во недель в году
    #     time.sleep(60*60*168) # кол-во часов в недели

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
