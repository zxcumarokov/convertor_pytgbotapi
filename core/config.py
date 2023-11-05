# Third Party Stuff
from sqlalchemy.engine import URL

TOKEN = "5991863328:AAHf0Fyz3rtMR8851RF3xfyqdzIYNNDbVnM"
# Вручную задаем данные из вашей ссылки
drivername = "postgresql"
username = "postgres"
password = "postgrespw"
host = "localhost"
port = 32771
database = "telegrambotapiconverter"

# Создаем объект URL
DB_URL = URL.create(
    drivername=drivername,
    username=username,
    host=host,
    database=database,
    port=port,
    password=password,
)
