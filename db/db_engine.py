# Third Party Stuff
from sqlalchemy import create_engine

# My Stuff
from core.config import DB_URL

engine = create_engine(DB_URL, echo=True)
