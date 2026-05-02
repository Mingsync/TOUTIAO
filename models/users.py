from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class User(Base):
    """用户模型类"""
    __tablename__ = "users"

    # 创建索引
    __table_args__ = (
        Index('username_unique', 'username', unique=True),  # 用户名唯一索引
        Index('phone_unique', 'phone', unique=True),  # 电话号码唯一索引
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="用户名")
    password:Mapped[str] = mapped_column(String(255), nullable=False, comment="用户密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="用户昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="用户头像URL")
    bio: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="用户简介")
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="用户邮箱")
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="用户电话号码")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, comment="用户性别")
    token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="访问令牌")
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="令牌过期时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    

    
    