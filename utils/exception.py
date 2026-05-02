from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


DeBUG_MODE = True

async def http_exception_handler(request:Request, exc:HTTPException):

    if DeBUG_MODE:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "发生错误，请稍后再试"}
        )
    
async def integerity_error_handler(request:Request, exc:IntegrityError):

    """处理数据库完整性约束错误"""
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    # 判断具体的约束错误类型
    if "UNIQUE constraint failed" in error_msg:
        detail = "数据已存在，违反唯一约束"
    elif "NOT NULL constraint failed" in error_msg:
        detail = "缺少必填字段，违反非空约束"
    else:
        detail = "数据完整性错误"

    # 开发模式下返回详细错误信息
    error_data = None

    if DeBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": error_msg,
            "path": request.url.path
        }
    else:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": detail
        }
    return JSONResponse(
        status_code=400,
        content={"detail": detail, "error": error_data}
    )

async def sqlalchemy_error_handler(request:Request, exc:SQLAlchemyError):

    """处理SQLAlchemy相关错误"""
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    detail = "数据库错误，请稍后再试"

    # 开发模式下返回详细错误信息
    error_data = None

    if DeBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": error_msg,
            "path": request.url.path
        }
    else:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": detail
        }
    return JSONResponse(
        status_code=500,
        content={"detail": detail, "error": error_data}
    )

async def general_exception_handler(request:Request, exc:Exception):

    """处理其他未捕获的异常"""
    error_msg = str(exc)
    detail = "服务器发生错误，请稍后再试"

    # 开发模式下返回详细错误信息
    error_data = None

    if DeBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": error_msg,
            "path": request.url.path
        }
    else:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": detail
        }
    return JSONResponse(
        status_code=500,
        content={"detail": detail, "error": error_data}
    )