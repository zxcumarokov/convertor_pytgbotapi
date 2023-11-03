# Third Party Stuff
from sqlalchemy.engine import URL

TOKEN = "5991863328:AAHf0Fyz3rtMR8851RF3xfyqdzIYNNDbVnM"
DB_URL = URL.create(
    drivername="postgresql+psycopg",
    username="sumarokov",
    host="localhost",
    database="ivan",
    port=32769,
    password="Leonard0",
)
