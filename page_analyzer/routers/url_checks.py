__all__ = ["url_checks_bp"]


from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, flash, redirect, request, url_for
from pydantic_core import ValidationError
from requests.exceptions import RequestException
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug import Response

from page_analyzer.database.models.url_checks import UrlCheck as UrlCheckModel
from page_analyzer.database.models.urls import Url as UrlModel
from page_analyzer.schemas.url_checks import UrlCheckCreate
from page_analyzer.schemas.urls import Url as UrlSchema
from page_analyzer.utilities.site_checker import check_site

url_checks_bp = Blueprint("url_checks", __name__)


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
        form_data = UrlCheckCreate(url_id=url_id)  # type: ignore
    except ValidationError as validation_error:
        for error in validation_error.errors():
            flash(f"Произошла ошибка при проверке: {error['msg']}.", "error")
        return redirect(request.referrer)

    url_existence_check_statement = select(UrlModel).where(UrlModel.id == form_data.url_id)
    url_db = db.execute(url_existence_check_statement).scalars().first()
    if url_db is None:
        flash("Произошла ошибка при проверке: сайт не найден", "error")
        return redirect(url_for("urls.get_url"))

    try:
        url = UrlSchema.model_validate(url_db)
    except ValidationError as validation_error:
        for error in validation_error.errors():
            flash(f"Произошла ошибка при проверке: {error['msg']}.", "error")
        return redirect(url_for("urls.get_url", url_id=url_id))

    try:
        url_check_result = check_site(url)
    except RequestException:
        flash("Произошла ошибка при проверке", "error")
        return redirect(url_for("urls.get_url", url_id=url_id))

    url_check_db = UrlCheckModel(url_id=form_data.url_id, **url_check_result.model_dump())
    db.add(url_check_db)
    db.commit()

    flash("Страница успешно проверена", "success")
    return redirect(url_for("urls.get_url", url_id=url_id))
