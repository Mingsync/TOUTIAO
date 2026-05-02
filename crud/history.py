from sqlalchemy.ext.asyncio import AsyncSession

# 检查是否添加了某条浏览历史
from sqlalchemy import delete, func, select

from models.history import History
from models.news import News


async def is_history_added(db: AsyncSession, user_id: int, news_id: int):
    # 这里可以根据用户ID和新闻ID查询是否已经添加了浏览历史
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None

async def add_history_record(db: AsyncSession, user_id: int, news_id:int):
    # 这里通过user_id和news_id添加浏览历史记录
    history_record = History(user_id=user_id, news_id=news_id)
    db.add(history_record)
    await db.commit()
    await db.refresh(history_record)
    return history_record


async def remove_history_record(db:AsyncSession, user_id:int,  news_id:int):
    delete_stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount > 0  # 返回受影响的行数，通常为1表示成功删除浏览历史记录


async def get_history_list_by_user(db:AsyncSession, user_id:int, page:int=1, page_size:int=10):
    # 根据user_id查询历史浏览列表
    count_query = select(func.count()).where(History.user_id == user_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = select(News, History.created_at.label("view_time"), History.id.label("history_id"))\
            .join(News, News.id == History.news_id).order_by(History.created_at.desc())\
            .offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    history_list = []
    for news, view_time, history_id in result.all():
        history_list.append({
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "category_id": news.category_id,
            "views": news.view,
            "publish_time": news.publish_time,
            "view_time": view_time,
            "history_id": history_id
        })
    return {"total": total, "history": history_list}


async def remove_all_history(db:AsyncSession, user_id:int):
    delete_stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount > 0  # 返回受影响的行数，通常为1表示成功删除所有浏览历史记录
        