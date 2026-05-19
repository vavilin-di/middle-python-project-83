from os import getenv

from dishka import make_container
from dishka.integrations.flask import setup_dishka
from dotenv import load_dotenv
from flask import Flask

from page_analyzer.database.connection import DBProvider
from page_analyzer.routers import index_bp, urls_bp

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

container = make_container(DBProvider())
setup_dishka(container=container, app=app, auto_inject=True)

app.register_blueprint(index_bp)
app.register_blueprint(urls_bp, url_prefix="/urls")
