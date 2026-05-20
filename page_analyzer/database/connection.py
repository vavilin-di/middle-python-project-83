__all__ = ["DATABASE_URL", "Base", "DBProvider"]

from collections.abc import Iterator
from os import getenv

from dishka import Provider, Scope, provide
from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DATABASE_URL = make_url(getenv("DATABASE_URL", "")).set(drivername="postgresql+psycopg2")


class Base(DeclarativeBase): ...


# DI-контейнер для подключений к базе данных
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
