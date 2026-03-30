from os import getenv

from dotenv import load_dotenv
from flask import Flask

from page_analyzer.index import index_bp

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

app.register_blueprint(index_bp)
