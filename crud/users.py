import uuid
from datetime import datetime, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
from utils.security import get_password_hash, verify_password

async def get_user_info_by_username(username: str, db: AsyncSession):
    # 这里可以根据username查询用户信息
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user_info = result.scalar_one_or_none()
    return user_info

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先进行密码加密
    user_data.password = get_password_hash(user_data.password)

    new_user = User(username=user_data.username, password=user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# 生成访问令牌
async def create_access_token(db: AsyncSession, user_id: int):
    # 这里可以使用 JWT 或其他方式生成访问令牌
    token = uuid.uuid4()  # 生成一个随机的访问令牌
    expires_at = datetime.now() + timedelta(days=7)  # 设置令牌过期时间
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = User(id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    return token


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user_info = await get_user_info_by_username(username=username, db=db)
    if not user_info:
        return None
    # 这里可以添加密码验证逻辑
    if not verify_password(password, user_info.password):
        return None
    return user_info

# 根据Token查询用户信息
async def get_user_info_by_token(db: AsyncSession, token: str):
    # 这里可以根据访问令牌查询用户信息
    query = select(User).where(User.token == token)
    result = await db.execute(query)
    user_info = result.scalar_one_or_none()

    if not user_info or user_info.expires_at < datetime.now():
        return None
    
    query = select(User).where(User.id == user_info.id)
    result = await db.execute(query)
    user_info = result.scalar_one_or_none()
    return user_info

# 更新用户信息

async def update_user_info(db:AsyncSession, user_id:int, update_data:UserUpdateRequest):
    stmt = update(User).where(User.id == user_id).values(
        nickname=update_data.nick_name,
        avatar=update_data.avatar,
        gender=update_data.gender,
        bio=update_data.bio)
    await db.execute(stmt)
    await db.commit()


# 修改用户密码: 验证及密码——>新密码加密->数据库更新
async def change_password(db:AsyncSession, user:User, old_password:str, new_password:str):
    if not security.verify_password(old_password, user.password):  # 验证旧密码
        return False
    
    user.password = security.get_password_hash(new_password)  # 更新数据库中的密码
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True