from aiogram import executor
from create import dp


async def start_bot(_):
    print('Online')


async def finish(_):
    print('Offline')


from handlers import client, anketa

client.reg_client_handlers(dp)
anketa.register_handlers_zayava(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot, on_shutdown=finish)
    