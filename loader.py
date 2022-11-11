import redis
import logging
from config import load_config

from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = load_config()

with redis.Redis(host=config.redis.redis_host, port=config.redis.redis_port) as redis_client:
    logger.info("redis is connecting")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
