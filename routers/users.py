from fastapi import APIRouter, Depends, HTTPException, Query
from configs.db_conf import get_db
from crud import users
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserAuthResponse, UserChangePasswordRequest, UserInfoResponse, UserRequest, UserUpdateRequest
from utils.auth import get_current_user
from utils.response import success_response

# 创建一个ApiRouter路由器实例
router = APIRouter(prefix="/api/users",tags=["users"])



@router.post("/register")
async def register_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册接口
    """
    user_info = await users.get_user_info_by_username(username=user_data.username, db=db)
    if user_info:
        raise HTTPException(status_code=400, detail="用户名已存在")
    new_user = await users.create_user(db=db, user_data=user_data)
    token = await users.create_access_token(db=db, user_id=new_user.id)

    user_info = UserInfoResponse.model_validate(new_user)
    response_data = UserAuthResponse(token=token, user_info=user_info)
    return success_response(data=response_data, message="注册成功")


@router.post("/login")

async def login_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    """
    user = await users.authenticate_user(db=db, username=user_data.username, password=user_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = await users.create_access_token(db=db, user_id=user.id)
    user_info = UserInfoResponse.model_validate(user)
    response_data = UserAuthResponse(token=token, user_info=user_info)
    return success_response(data=response_data, message="登录成功")
    

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    获取当前用户信息接口
    """
    return success_response(data=UserInfoResponse.model_validate(current_user), message="获取用户信息成功")



@router.put("/update")
async def update_user_info(current_user: dict = Depends(get_current_user), 
                           update_data: UserUpdateRequest = None,
                           db: AsyncSession = Depends(get_db)):
    """
    更新当前用户信息接口
    """
    # 这里可以根据update_data更新用户信息
    # 需要实现一个函数来更新用户信息
    return success_response(data=UserInfoResponse.model_validate(current_user), message="更新用户信息成功")

@router.put("/change-password")
async def change_user_password(current_user: dict = Depends(get_current_user), 
                               password_data: UserChangePasswordRequest = None,
                               db: AsyncSession = Depends(get_db)):
    """
    修改当前用户密码接口
    """
    # 这里可以根据password_data修改用户密码
    # 需要实现一个函数来修改用户密码
    res_change_password = await users.change_password(db=db, user=current_user, old_password=password_data.old_password, new_password=password_data.new_password)
    if not res_change_password:
        raise HTTPException(status_code=400, detail="旧密码错误")
    return success_response(message="修改密码成功")


