__all__ = ["url_checks_bp"]


from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, flash, redirect, request, url_for
from pydantic_core import ValidationError
from requests.exceptions import RequestException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from werkzeug import Response

from page_analyzer.database.models import Url as UrlModel
from page_analyzer.database.models import UrlCheck as UrlCheckModel
from page_analyzer.schemas.url_checks import UrlCheckCreate
from page_analyzer.schemas.urls import Url as UrlSchema
from page_analyzer.utilities.site_checker import check_site
from page_analyzer.utilities.validation_helpers import flash_validation_errors

url_checks_bp = Blueprint("url_checks", __name__)


class UrlRetrievalError(Exception): ...


@url_checks_bp.route("/", methods=["POST"])
@inject
def create_url_check(url_id: int, db: FromDishka[Session]) -> Response | str:
    """Создаёт новую проверку для указанного URL.

    Обрабатывает POST-запрос на создание проверки сайта. Функция выполняет
    следующие шаги:
    1. Валидирует переданный url_id с помощью схемы UrlCheckCreate.
    2. Проверяет существование URL в базе данных.
    3. Получает данные сайта через утилиту check_site.
    4. Сохраняет результаты проверки в таблицу url_checks.

    Args:
        url_id (int): Идентификатор URL, для которого создаётся проверка.
        db (FromDishka[Session]): Сессия базы данных, внедрённая через Dishka.

    Returns:
        Response | str: Редирект на страницу детального просмотра URL
        (urls.get_url) с соответствующим flash-сообщением.
    """
    try:
        form_data = UrlCheckCreate(url_id=url_id)
    except ValidationError as validation_error:
        flash_validation_errors(validation_error, "Произошла ошибка при проверке")
        return redirect(request.referrer)

    try:
        url = _get_url(db, form_data.url_id)
    except UrlRetrievalError:
        return redirect(url_for("urls.get_url", url_id=form_data.url_id))

    try:
        url_check_result = check_site(url)
    except RequestException:
        flash("Произошла ошибка при проверке", "error")
        return redirect(url_for("urls.get_url", url_id=form_data.url_id))

    url_check_db = UrlCheckModel(url_id=form_data.url_id, **url_check_result.model_dump())

    try:
        db.add(url_check_db)
        db.commit()
    except SQLAlchemyError:
        flash("Произошла ошибка при проверке", "error")
        db.rollback()
        return redirect(url_for("urls.get_url", url_id=url_id))

    flash("Страница успешно проверена", "success")
    return redirect(url_for("urls.get_url", url_id=url_id))


def _get_url(db: Session, url_id: int) -> UrlSchema:
    """Получает запись существующего URL из базы данных по идентификатору.

    Вспомогательная функция для извлечения записи URL из базы данных
    с обработкой ошибок и валидацией.

    Args:
        db (FromDishka[Session]): Сессия базы данных, внедрённая через Dishka.
        url_id (int): Идентификатор URL для поиска.

    Returns:
        UrlSchema: Валидированная схема URL, соответствующая записи в базе.

    Raises:
        UrlRetrievalError: Если произошла ошибка SQLAlchemy, запись не найдена
        или валидация схемы не удалась.
    """

    url_existence_check_statement = select(UrlModel).where(UrlModel.id == url_id)
    try:
        url_db = db.execute(url_existence_check_statement).scalars().first()
    except SQLAlchemyError as error:
        flash("Произошла ошибка при проверке", "error")
        db.rollback()
        raise UrlRetrievalError from error

    if url_db is None:
        flash("Произошла ошибка при проверке: сайт не найден", "error")
        raise UrlRetrievalError

    try:
        return UrlSchema.model_validate(url_db)
    except ValidationError as validation_error:
        flash_validation_errors(validation_error, "Произошла ошибка при проверке")
        raise UrlRetrievalError from validation_error
