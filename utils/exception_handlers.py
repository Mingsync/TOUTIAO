from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from utils.exception import general_exception_handler


def register_exception_handlers(app):
    from .exception import http_exception_handler, integerity_error_handler, sqlalchemy_error_handler

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, integerity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)