# Standard Library
import logging
import os

# Third Party Stuff
from sqlalchemy import text
from sqlalchemy.orm import Session

# My Stuff
from db.db_engine import engine

logging.basicConfig(level=logging.INFO)
# TABLES = [
#     "db/directions.sql",
#     "db/phrases.sql",
# ]
FOLDERS = [
    "db/scripts/",
]


def main():
    print("update database")
    with Session(engine) as session:
        # update db from files in FOLDERS
        for folder in FOLDERS:
            # get all files in folder
            files = os.listdir(folder)
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext != ".sql":
                    continue
                full_path = os.path.join(folder, file)
                if os.path.isfile(full_path):
                    with open(full_path, "r") as table_file:
                        logging.info(f"update table {full_path}")
                        query = table_file.read()
                        session.execute(text(query))

        session.commit()


if __name__ == "__main__":
    main()
