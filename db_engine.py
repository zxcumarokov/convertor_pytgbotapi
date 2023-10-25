import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read("alembic.ini")
url = config["alembic"]["sqlalchemy.url"]
engine = create_engine(url)
