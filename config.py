from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    pg_host: str
    pg_port: str
    pg_user: str
    pg_password: str
    pg_database: str


@dataclass
class TgBot:
    token: str


@dataclass
class RedisConfig:
    redis_host: str
    redis_port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig


def load_config(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN")
        ),
        db=DbConfig(
            pg_host=env.str("POSTGRES_HOST"),
            pg_port=env.str("PG_PORT"),
            pg_user=env.str("POSTGRES_USER"),
            pg_password=env.str("POSTGRES_PASSWORD"),
            pg_database=env.str("POSTGRES_DB")
        ),
        redis=RedisConfig(
            redis_host=env.str("REDIS_HOST"),
            redis_port=env.str("REDIS_PORT")
        )
    )
