
from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase


class FavoriteCheckReponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite", description="是否已收藏")


class FavoriteAddRequest(BaseModel):
    news_id: int= Field(..., alias="newsId", description="新闻ID")


# 规划两个类： 一个是新闻模型类 + 收藏的模型类
class FavoriteNewsItemResponse(NewsItemBase):
    """收藏新闻项响应模型类"""
    favorite_id: int = Field(..., alias="favoriteId", description="收藏ID")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")

    model_config = ConfigDict(
        from_attributes=True, # 支持从ORM对象创建模型实例
        populate_by_name=True # 支持通过别名和字段名填充模型
    )


# 收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list: List[FavoriteNewsItemResponse] = Field(..., description="收藏新闻列表")
    total:int = Field(..., description="收藏总数")
    has_more: bool = Field(..., alias="hasMore", description="是否有更多数据")

    model_config = ConfigDict(
        from_attributes=True, # 支持从ORM对象创建模型实例
        populate_by_name=True # 支持通过别名和字段名填充模型
    )