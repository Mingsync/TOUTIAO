from fastapi import FastAPI
from routers import favorite, history, news, users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers


app = FastAPI()

orgins = [
    "http://localhost:3000",
    "http://localhost:3001"
]

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# 挂载路由，注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)