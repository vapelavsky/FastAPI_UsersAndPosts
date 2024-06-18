from config import (
    db_host,
    db_name,
    db_password,
    db_port,
    db_user,
    db_driver,
    arguments,
)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, OperationalError
from db.db_base import Base


def create_tables_if_not_exists(db_engine, base):
    tables = []
    for table in base.metadata.tables.keys():
        try:
            base.metadata.tables[table].create(bind=db_engine)
            print(f"Table '{table}' created.")
        except ProgrammingError:
            tables.append(table)
        except OperationalError:
            pass
    if len(tables) != 0:
        print("All tables were already created.")
    else:
        print(f"Tables {', '.join(tables)} already exist.")


engine = create_engine(
        "sqlite:///./sql_app.db", connect_args={"check_same_thread": False}
    )
create_tables_if_not_exists(engine, Base)
with engine.connect() as connection:
    connection.execute(text("PRAGMA foreign_keys=ON"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
