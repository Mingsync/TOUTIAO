from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UniqueConstraint, Index
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    id: Mapped[Optional[int]] = None
    created_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)



class History(Base):
    """浏览历史ORM模型类"""
    __tablename__ = "history"
    
    """创建索引"""
    __table_args__ = (
        UniqueConstraint("user_id","news_id",name="user_news_history_unique"),
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(nullable=False, comment="新闻ID")


    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"