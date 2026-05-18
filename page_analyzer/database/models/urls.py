from datetime import datetime

from sqlalchemy import Date, String, func
from sqlalchemy.orm import Mapped, mapped_column

from page_analyzer.database.connection import Base


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(Date(), nullable=False, server_default=func.now())
