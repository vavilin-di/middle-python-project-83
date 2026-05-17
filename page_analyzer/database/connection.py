from os import getenv

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=int(getenv("DB_PORT", "5432")),
    database=getenv("DB_DATABASE"),
)

engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(engine, expire_on_commit=False, class_=Session)


class Base(DeclarativeBase): ...
