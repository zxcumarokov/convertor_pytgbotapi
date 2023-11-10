# Third Party Stuff
from sqlalchemy.engine import URL

TOKEN = "6862002582:AAHKSgSgceR8LXEMV3cMU7G6cQ-IbOOpp9U"
# Вручную задаем данные из вашей ссылки
drivername = "postgresql"
username = "postgres"
password = "postgrespw"
host = "localhost"
port = 32770
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


