from typing import Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """用户信息基础模型类"""
    nick_name: Optional[str] = Field(None, max_length= 50, description="用户昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="用户性别")
    bio: Optional[str] = Field(None, max_length=255, description="用户简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True, # 支持从ORM对象创建模型实例

    )


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(..., alias="user_info", description="用户信息")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias / field name 都可以使用
        from_attributes=True, # 支持从ORM对象创建模型实例
    )


class UserUpdateRequest(UserInfoBase):
    """用户信息更新请求模型类"""
    nick_name: Optional[str] = Field(None, max_length= 50, description="用户昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="用户性别")
    bio: Optional[str] = Field(None, max_length=255, description="用户简介")



class UserChangePasswordRequest(BaseModel):
    """用户修改密码请求模型类"""
    old_password: str = Field(..., alias="old_password", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="new_password", description="新密码")