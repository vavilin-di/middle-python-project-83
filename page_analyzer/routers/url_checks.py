__all__ = ["url_checks_bp"]


from flask import Blueprint, flash, redirect, request, url_for
from pydantic_core import ValidationError
from sqlalchemy.orm import Session
from requests.exceptions import HTTPError
from sqlalchemy import select
from werkzeug import Response
from dishka.integrations.flask import FromDishka, inject

from page_analyzer.database.models.url_checks import UrlCheck as UrlCheckModel
from page_analyzer.database.models.urls import Url as UrlModel
from page_analyzer.schemas.url_checks import UrlCheckCreate
from page_analyzer.schemas.urls import Url as UrlSchema
from page_analyzer.utilities.site_checker import check_site

url_checks_bp = Blueprint("url_checks", __name__)


@url_checks_bp.route("/", methods=["POST"])
@inject
def create_url_check(url_id: int, db: FromDishka[Session]) -> Response | str:
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
    except HTTPError as error:
        flash(f"Произошла ошибка при проверке: {error}", "error")
        return redirect(url_for("urls.get_url", url_id=url_id))
    except Exception:
        flash("Произошла ошибка при проверке", "error")
        return redirect(url_for("urls.get_url", url_id=url_id))

    url_check_db = UrlCheckModel(url_id=form_data.url_id, **url_check_result.model_dump())
    db.add(url_check_db)
    db.commit()

    flash("Страница успешно проверена", "success")
    return redirect(url_for("urls.get_url", url_id=url_id))
