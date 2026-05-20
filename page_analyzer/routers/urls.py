__all__ = ["urls_bp"]

from http import HTTPStatus

from dishka.integrations.flask import FromDishka, inject
from flask import Blueprint, flash, redirect, render_template, request, url_for
from pydantic_core import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from werkzeug import Response

from page_analyzer.database.models.url_checks import UrlCheck as UrlCheckModel
from page_analyzer.database.models.urls import Url as UrlModel
from page_analyzer.schemas.urls import Url as UrlSchema
from page_analyzer.schemas.urls import UrlCreate
from page_analyzer.schemas.urls import UrlList as UrlListSchema

from .url_checks import url_checks_bp

urls_bp = Blueprint("urls", __name__)

urls_bp.register_blueprint(url_checks_bp, url_prefix="/<int:url_id>/checks")


@urls_bp.route("/", methods=["GET"])
@inject
def get_all_urls(db: FromDishka[Session]) -> Response | str:
    """
    Обрабатывает GET-запрос для получения списка всех URL.

    Извлекает все URL из базы данных вместе с информацией о последней проверке
    (дата последней проверки и статус код). Результаты сортируются по ID в
    порядке убывания.

    Args:
        db (FromDishka[Session]): Сессия базы данных, внедряемая через Dishka.

    Returns:
        Response | str: редирект на index.index при возникновении ошибок при работе с БД,
        в противном случае - HTML-страница со списком URL (шаблон urls/urls.html).
    """
    last_url_check_subquery = select(
        UrlCheckModel.url_id,
        UrlCheckModel.created_at.label("last_check"),
        UrlCheckModel.status_code,
        func.row_number()
        .over(partition_by=UrlCheckModel.url_id, order_by=UrlCheckModel.created_at.desc())
        .label("row_number"),
    ).subquery()

    statement = (
        select(UrlModel.id, UrlModel.name, last_url_check_subquery.c.last_check, last_url_check_subquery.c.status_code)
        .select_from(UrlModel)
        .outerjoin(
            last_url_check_subquery,
            (UrlModel.id == last_url_check_subquery.c.url_id) & (last_url_check_subquery.c.row_number == 1),
        )
        .order_by(UrlModel.id.desc())
    )
    db_url_mappings = db.execute(statement).mappings().all()
    urls = []
    try:
        urls = [UrlListSchema(**db_url_mapping).model_dump() for db_url_mapping in db_url_mappings]
    except ValidationError as validation_error:
        for error in validation_error.errors():
            flash(f"Ошибка: {error['msg']}.", "error")
    return render_template("urls/urls.html", urls=urls)


@urls_bp.route("/<int:url_id>")
@inject
def get_url(url_id: int, db: FromDishka[Session]) -> Response | str:
    """
    Обрабатывает GET-запрос для получения детальной информации об одном URL.

    Ищет URL по его ID в базе данных. Если URL не найден, отображает ошибку
    и перенаправляет на список всех URL. Если найден, валидирует данные через
    Pydantic и отображает страницу с деталями URL.

    Args:
        url_id (int): Идентификатор URL в базе данных.
        db (FromDishka[Session]): Сессия базы данных, внедряемая через Dishka.

    Returns:
        Response | str: Если URL не найден, возвращает редирект (Response).
        Иначе возвращает HTML-страницу с деталями URL (шаблон urls/url.html).

    """
    statement = select(UrlModel).where(UrlModel.id == url_id)
    db_url = db.execute(statement).scalars().first()
    if db_url is None:
        flash("Ошибка: сайт не найден", "error")
        return redirect(url_for("urls.get_all_urls"))
    try:
        url = UrlSchema.model_validate(db_url)
    except ValidationError as validation_error:
        for error in validation_error.errors():
            flash(f"Ошибка: {error['msg']}.", "error")
        return redirect(url_for("urls.get_all_urls"))
    return render_template("urls/url.html", url=url.model_dump())


@urls_bp.route("", methods=["POST"])
@inject
def create_url(db: FromDishka[Session]) -> Response | tuple[str, int]:
    """
    Обрабатывает POST-запрос для создания нового URL.

    Принимает URL из формы, валидирует его с помощью Pydantic. Если URL некорректен,
    возвращает ошибку 422. Если URL уже существует в базе, перенаправляет на его
    страницу. Иначе создает новую запись в базе данных.

    Args:
        db (FromDishka[Session]): Сессия базы данных, внедряемая через Dishka.

    Returns:
        Response | tuple[str, int]: При успехе - редирект на страницу созданного URL.
        При ошибке валидации - кортеж (HTML-страница, статус 422).
        При ошибке базы данных - редирект на список всех URL.
    """

    try:
        form_data = UrlCreate(name=request.form["url"])  # type: ignore
    except ValidationError:
        flash("Некорректный URL", "error")
        return render_template("index/index.html"), HTTPStatus.UNPROCESSABLE_ENTITY

    url_name = str(form_data.name)
    check_existence_statement = select(UrlModel).where(UrlModel.name == url_name)

    db_url = UrlModel(name=url_name)
    existing_db_url = db.execute(check_existence_statement).scalars().first()
    if existing_db_url:
        flash("Страница уже существует", "error")
        return redirect(url_for("urls.get_url", url_id=existing_db_url.id))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("urls.get_url", url_id=db_url.id))
