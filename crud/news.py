from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import func, select, update



async def get_categories(db: AsyncSession, skip: int =0, limit: int =10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int =0, limit: int =10):
    # 这里可以根据category_id查询新闻列表
    # 例如：stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # result = await db.execute(stmt)
    # news_list = result.scalars().all()
    # return news_list
    staticmethod = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(staticmethod) 
    news_list = result.scalars().all()
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    news_count = result.scalars().first()
    return news_count

async def get_news_detail(db: AsyncSession, news_id: int):
    # 这里可以根据news_id查询新闻详情
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
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
