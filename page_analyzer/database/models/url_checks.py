__all__ = ["UrlCheck"]

from datetime import datetime

from sqlalchemy import Date, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from page_analyzer.database.connection import Base
from page_analyzer.database.models.urls import Url


class UrlCheck(Base):
    __tablename__ = "url_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("urls.id"), nullable=False)
    status_code: Mapped[int] = mapped_column(nullable=True)
    h1: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(Date(), nullable=False, server_default=func.now())
    url: Mapped[Url] = relationship("Url", back_populates="checks")
