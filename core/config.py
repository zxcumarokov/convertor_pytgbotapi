# Third Party Stuff
from sqlalchemy.engine import URL

TOKEN = "5991863328:AAHf0Fyz3rtMR8851RF3xfyqdzIYNNDbVnM"# Замените следующие переменные вашими данными# Замените следующие переменные вашими данными
drivername = "postgresql"
username = "postgres"
password = "postgrespw"
host = "localhost"
port = 5433  # Это порт, который вы пробросили с хоста на контейнер
database = "convtgbot"
# Создаем объект URL
DB_URL = URL.create(
    drivername=drivername,
    username=username,
    host=host,
    database=database,
    port=port,
    password=password,
)