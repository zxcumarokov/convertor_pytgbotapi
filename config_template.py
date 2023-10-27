# Third Party Stuff
from sqlalchemy.engine import URL

TOKEN = "TOKEN"
DB_URL = URL.create(
    drivername="postgresql+psycopg",
    username="sumarokov",
    host="localhost",
    database="ivan",
    port=32768,
    password="Leonard0",
)
