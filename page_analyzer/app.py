from os import getenv

from dotenv import load_dotenv
from flask import Flask

from page_analyzer.routers import index_bp, urls_bp

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

app.register_blueprint(index_bp)
app.register_blueprint(urls_bp, url_prefix="/urls")
