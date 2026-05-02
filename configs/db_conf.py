from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine



ASYNC_DATABASE_URL = "mysql+aiomysql://mwei_std:123456@localhost:3306/fastapi?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(ASYNC_DATABASE_URL, 
                             echo=True, # 启用SQL日志输出
                             pool_size=10,
                             max_overflow=20,)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(bind=engine, 
                   expire_on_commit=False, # 事务提交后不自动过期对象
                   class_=AsyncSession)


# 依赖项，用户获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 提交事务
        except Exception as e:
            await session.rollback()  # 回滚事务
            raise e
        finally:
            await session.close()  # 关闭会话
            

