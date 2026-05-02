# 整合，根据Token查询用户，返回用户
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_conf import get_db
from crud.users import get_user_info_by_token


async def get_current_user(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    
    token = authorization.split(" ")[1] if " " in authorization else authorization
    # 这里可以根据访问令牌查询用户信息
    user = await get_user_info_by_token(db=db, token=token)
    if not user:
        raise HTTPException(status_code=401, detail="无效的访问令牌")
    
    return user


    
