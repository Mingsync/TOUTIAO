from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from sqlalchemy import delete, func, select

from models.news import News

# 查询用户是否已收藏某条新闻，当前用户是否收藏了某条新闻
async def is_news_favorite(db:AsyncSession, user_id:int, news_id:int):
    select_stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(select_stmt)

    return result.scalar_one_or_none() is not None


async def add_favorite_by_user(db: AsyncSession, user_id: int, news_id: int):
    news_favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(news_favorite)
    await db.commit()
    await db.refresh(news_favorite)
    return news_favorite


async def remove_favorite_by_user(db: AsyncSession, user_id: int, news_id: int):
    stmt =  delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_favorite_list_by_user(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id")).join(Favorite, News.id == Favorite.news_id)\
        .where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    favorites = []
    for news, favorite_time, favorite_id in result.all():
        favorites.append({
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "created_at": news.created_at,
            "favorite_time": favorite_time,
            "favorite_id": favorite_id
        })  
    return {"total": total, "favorites": favorites}


async def remove_all_favorites(db: AsyncSession, user_id:int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
