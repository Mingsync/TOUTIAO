from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsItemBase(BaseModel):
    id: int
    title: str
    description:str
    image:Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = None
    views:int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )