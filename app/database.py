import os
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=SQL_ECHO, connect_args=connect_args)

# Enable SQLite Foreign Key constraints (ON DELETE / ON UPDATE)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def init_db() -> None:
    # Creates tables on app startup.
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    # Dependency that injects a database session per HTTP request.
    with Session(engine) as session:
        yield session