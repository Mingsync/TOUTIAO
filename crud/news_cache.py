from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import func, select, update
from configs.news_cache import get_cache_news_detail, get_cache_news_list, \
get_cached_categories, set_cache_news_list, set_cached_categories, set_cache_news_detail
from fastapi.encoders import jsonable_encoder
from schemas.base import NewsItemBase

async def get_categories(db: AsyncSession, skip: int =0, limit: int =10):
    cached_categories = await get_cached_categories()
    if cached_categories is not None:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    if categories:
        jsonable_encoder(categories)
        await set_cached_categories(categories, expire=3600)  # 假设缓存过期时间为3600秒
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int =0, limit: int =10):
    # 这里可以根据category_id查询新闻列表
    # 例如：stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # result = await db.execute(stmt)
    # news_list = result.scalars().all()
    # return news_list
    # 尝试从缓存中获取新闻列表数据
    cached_news_list = await get_cache_news_list(category_id, skip // limit + 1, limit)
    if cached_news_list is not None:
        # return [jsonable_encoder(news) for news in cached_news_list]
        return [News(**news) for news in cached_news_list]


    staticmethod = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(staticmethod) 
    news_list = result.scalars().all()

    # 将查询结果写入缓存，设置过期时间为1小时（3600秒）
    if news_list:
        # jsonable_news_list = [jsonable_encoder(news) for news in news_list]
        # await set_cache_news_list(category_id, skip // limit + 1, jsonable_news_list, expire=3600)
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, skip // limit + 1, limit, news_data, expire=3600)
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    news_count = result.scalars().first()
    return news_count

async def get_news_detail(db: AsyncSession, news_id: int):
    # 这里可以根据news_id查询新闻详情
    cached_news_detail =  await get_cache_news_detail(news_id)
    if cached_news_detail is not None:
        return [News(**news) for news in cached_news_detail][0]

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    if news_detail:
        # news_data = [jsonable_encoder(news) for news in [news_detail]]
        news_data = [NewsItemBase.model_validate(news).model_dump(mode="json", by_alias=False) for news in [news_detail]]
        await set_cache_news_detail(news_id, news_data, expire=3600)
    return news_detail


async def increment_news_view(db: AsyncSession, news_id: int):
    # 增加新闻浏览量
    stmt = update(News).where(News.id == news_id).values(view=News.view + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0  # 返回受影响的行数，通常为1表示成功增加浏览量

async def get_related_news(db: AsyncSession, category_id: int, exclude_news_id: int, limit: int = 5):
    # 获取相关的新闻列表，排除当前新闻
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != exclude_news_id
    ).order_by(News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [
        {
            "id": news.id,
            "title": news.title,
            "publish_time": news.publish_time,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "view": news.view
        }
        for news in related_news
    ]
