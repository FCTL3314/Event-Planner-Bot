import aiogram

from data.config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot=bot, storage=storage)
