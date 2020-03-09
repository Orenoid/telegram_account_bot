import logging

from flask import Flask
from flask.logging import default_handler

from app.models import db
from app.webhook import telegram_bp
from app.utils import multilog
from app.utils.error import handle_exception
from config import config_map


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    @app.route('/', endpoint='ping_pong')
    def ping_pong():
        return "I'm still alive."

    db.init_app(app)
    register_logger(app)

    app.register_blueprint(telegram_bp, url_prefix='/telegram')

    app.register_error_handler(Exception, handle_exception)

    return app


def register_logger(app: Flask):
    # 写入日志文件
    app.logger.removeHandler(default_handler)
    handler = multilog.MyLoggerHandler('flask', encoding='UTF-8', when='H')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # 写入控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.INFO)