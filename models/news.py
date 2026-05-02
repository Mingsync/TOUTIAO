from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String


class Base(DeclarativeBase):
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now,comment="更新时间")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="分类名称")
    description: Mapped[str] = mapped_column(String(255), nullable=True, comment="分类描述")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', description='{self.description}')>"
    
class News(Base):
    __tablename__ = "news"

    # 创建索引，提升查询性能
    __table_args__ =(
        Index("fk_category_id", "category_id"), # 高频查询场景
        Index("idx_publish_time", "publish_time"), # 按照发布时间排序
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    content: Mapped[str] = mapped_column(String(2000), nullable=False, comment="新闻内容")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), comment="分类ID")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")
    description: Mapped[str] = mapped_column(String(255), nullable=True, comment="新闻描述")
    image: Mapped[str] = mapped_column(String(255), nullable=True, comment="新闻图片URL")
    author: Mapped[str] = mapped_column(String(100), nullable=True, comment="新闻作者")
    view: Mapped[int] = mapped_column(default=0, comment="浏览量")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', category_id={self.category_id})>"