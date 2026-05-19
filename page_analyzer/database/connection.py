from os import getenv
from typing import Iterator

from dishka import Provider, Scope, provide
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine.base import Engine
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


class Base(DeclarativeBase): ...


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self) -> Engine:
        return create_engine(DATABASE_URL, echo=True)

    @provide(scope=Scope.APP)
    def provide_session_maker(self, engine: Engine) -> sessionmaker:
        return sessionmaker(engine, expire_on_commit=False, class_=Session)

    @provide(scope=Scope.REQUEST)
    def provide_session(self, session_maker: sessionmaker) -> Iterator[Session]:
        with session_maker() as session:
            yield session
            session.close()
