from fastapi import APIRouter,Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news, news_cache
from configs.db_conf import get_db



# 创建一个ApiRouter路由器实例
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 10,db: AsyncSession = Depends(get_db)):
    # 获取数据库中的新闻分类数据 ->定义模型类 ->查询数据库 ->返回数据
    categories = await news_cache.get_categories(db=db, skip=skip, limit=limit)

    return {"code":200,
            "message":"success",
            "data":categories
    }

@router.get("/list")
async def get_news_list(category_id: int = Query(..., alias="categoryId"),
                         page: int = 1,
                         page_size: int = Query(..., le=100,alias="pageSize"),
                         db: AsyncSession = Depends(get_db)):
    # 获取数据库中的新闻列表数据 ->定义模型类 ->查询数据库 ->返回数据
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db=db, category_id=category_id, skip=offset, limit=page_size)
    total = await news_cache.get_news_count(db=db, category_id=category_id)
    hasMore = offset + page_size < total
    return {"code":200,
            "message":"获取新闻列表成功",
            "data":{"list":news_list,
                    "total":total,
                    "hasMore":hasMore,
                    }
    }

@router.get("/detail/{news_id}")
async def get_news_detail(news_id: int, db: AsyncSession = Depends(get_db)):
    # 获取数据库中的新闻详情数据 ->定义模型类 ->查询数据库 ->返回数据
    # 这里可以根据news_id查询新闻详情
    news_detail = await news.get_news_detail(db=db, news_id=news_id)
    if news_detail is None:
       raise HTTPException(status_code=404, detail="新闻未找到")
    # 增加新闻浏览量
    view_count = await news.increment_news_view(db=db, news_id=news_detail.id)
    if not view_count:
        raise HTTPException(status_code=500, detail="增加新闻浏览量失败")
    return {"code":200,
            "message":f"获取新闻详情成功，新闻ID为{news_id}",
            "data":{"id":news_id,
                    "title":news_detail.title,
                    "content":news_detail.content,
                    "category_id":news_detail.category_id,
                    "publish_time":news_detail.publish_time,
                    "description":news_detail.description,
                    "image":news_detail.image,
                    "author":news_detail.author,
                    "view":news_detail.view,
                    }
    }

@router.get("/related")
async def get_related_news(category_id: int = Query(..., alias="categoryId"),
                           exclude_news_id: int = Query(..., alias="excludeNewsId"),
                           limit: int = Query(5, le=20, alias="limit"),
                           db: AsyncSession = Depends(get_db)):
    # 获取相关的新闻列表，排除当前新闻
    related_news = await news.get_related_news(db=db, category_id=category_id, exclude_news_id=exclude_news_id, limit=limit)
    return {
        "code": 200,
        "message": "获取相关新闻成功",
        "data": related_news
    }
