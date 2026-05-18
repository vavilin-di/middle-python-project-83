from flask import Blueprint, flash, redirect, request, url_for
from pydantic_core import ValidationError
from sqlalchemy import exists, select
from werkzeug import Response

from page_analyzer.database.connection import session_factory
from page_analyzer.database.models.url_checks import UrlCheck as UrlCheckModel
from page_analyzer.database.models.urls import Url as UrlModel
from page_analyzer.schemas.url_checks import UrlCheckCreate

url_checks_bp = Blueprint("url_checks", __name__)


@url_checks_bp.route("/", methods=["POST"])
def create_url_check(url_id: int) -> Response | str:
    try:
        form_data = UrlCheckCreate(url_id=url_id)  # type: ignore
    except ValidationError as validation_error:
        for error in validation_error.errors():
            flash(f"Произошла ошибка при проверке: {error['msg']}.", "error")
        return redirect(request.referrer)

    url_existence_check_statement = select(exists(UrlModel).where(UrlModel.id == form_data.url_id))
    with session_factory() as session:
        if not session.execute(url_existence_check_statement).scalar_one_or_none():
            flash("Произошла ошибка при проверке: сайт не найден", "error")
            return redirect(url_for("urls.get_url"))
        url_check_db = UrlCheckModel(url_id=form_data.url_id)
        session.add(url_check_db)
        session.commit()

    flash("Страница успешно проверена", "success")
    return redirect(url_for("urls.get_url", url_id=url_id))
