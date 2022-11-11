from config import load_config

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

config = load_config()

DATABASE = {
    'drivername': 'postgresql',
    'host': config.db.pg_host,
    'port': config.db.pg_port,
    'username': config.db.pg_user,
    'password': config.db.pg_password,
    'database': config.db.pg_database
}

engine = create_engine(URL.create(**DATABASE))
Session = sessionmaker(bind=engine)
session = Session()









