from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(data=None, message="成功"):

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "code": 200,
            "message": message,
            "data": data
        })
    )