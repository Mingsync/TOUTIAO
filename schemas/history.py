from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase
from typing import List

class HistoryCheckResponse(BaseModel):
    is_viewed: bool = Field(..., alias="isViewed", description="是否已浏览")

class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")

class HistoryAddResponse(BaseModel):
    history_id: int = Field(..., description="浏览历史记录ID")


class HistoryRecordResponse(NewsItemBase):
    id: int = Field(..., description="浏览历史记录ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    viewed_time: str = Field(..., alias="viewedTime", description="浏览时间")

    model_config = ConfigDict(
        from_attributes=True, # 支持从ORM对象创建模型实例
        populate_by_name=True # 支持通过别名和字段名填充模型
    )

class HistoryListResponces(BaseModel):
    list: List[HistoryRecordResponse] = Field(..., description="浏览历史记录列表")
    total: int = Field(..., description="浏览历史记录总数")
    has_more: bool = Field(..., alias="hasMore", description="是否有更多数据")

    model_config = ConfigDict(
        from_attributes=True, # 支持从ORM对象创建模型实例
        populate_by_name=True # 支持通过别名和字段名填充模型
    )