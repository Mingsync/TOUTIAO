from configs.cache_conf import get_json_cache, set_cache
from typing import Any, List, Dict, Optional
CATEGORIES_KEY = "news:categories"
NEWS_LIST_KEY_PREFIX = "news_list"  # 新闻列表缓存的键前缀
NEWS_DETAIL_KEY_PREFIX = "news_detail"  # 新闻详情缓存的键前缀

# 获取新闻分类列表的缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

# 写入新闻分类缓存：缓存的数据，过期的时间
# 数据越稳定，缓存越持久
async def set_cached_categories(data:List[Dict[str,Any]], expire: int = 3600):
    return await set_cache(CATEGORIES_KEY, data, expire=expire)

# 写入缓存-新闻列表
async def set_cache_news_list(category_id:Optional[int],
                              page: int, 
                              page_size: int, 
                              data:List[Dict[str,Any]], 
                              expire: int = 3600):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY_PREFIX}{category_part}:{page}:{page_size}"
    return await set_cache(key, data, expire=expire)


# 读取缓存-新闻列表
async def get_cache_news_list(category_id:Optional[int],
                              page:int,
                              page_size:int):
    category_part = category_id if category_id is not None else "all"
    key=f"{NEWS_LIST_KEY_PREFIX}{category_part}:{page}:{page_size}"
    return await get_json_cache(key)


# 写入缓存-新闻详情
async def set_cache_news_detail(news_id: int,
                                data: List[Dict[str, Any]],
                                expire: int = 3600):
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    return await set_cache(key, data, expire=expire)


# 读取缓存-新闻详情
async def get_cache_news_detail(news_id: int):
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    return await get_json_cache(key)