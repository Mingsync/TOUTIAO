from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_conf import get_db
from crud.favority import add_favorite_by_user, get_favorite_list_by_user, is_news_favorite, remove_all_favorites, remove_favorite_by_user
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteCheckReponse, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response


router =  APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(news_id: int=Query(..., alias="newsId"),
                         user:User=Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    
    # 这里可以根据news_id和用户信息查询是否已收藏
    is_favorite = await is_news_favorite(db=db, user_id=user.id, news_id=news_id)

    return success_response(message="查询收藏状态成功", data=FavoriteCheckReponse(is_favorite=is_favorite))  


@router.post("/add")
async def add_favorite(
    favorite_request: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    result = await add_favorite_by_user(db=db, user_id=user.id, news_id=favorite_request.news_id)
    return success_response(message="添加收藏成功", data=result)


@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await remove_favorite_by_user(db=db, user_id=user.id, news_id=news_id)
    if not result:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return success_response(message="删除收藏成功", data=None)


@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户收藏列表接口
    """
    # 这里可以根据current_user查询用户的收藏列表
    # 需要实现一个函数来查询用户收藏列表
    result = await get_favorite_list_by_user(db=db, user_id=current_user.id, page=page, page_size=page_size)
    
    data = FavoriteListResponse(
        list=result["favorites"],
        total=result["total"],
        has_more=(page * page_size < result["total"])
    )
    return success_response(data=data, message="获取收藏列表成功")

@router.delete("/clear")
async def clear_favorites(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    清空用户收藏接口
    """
    result = await remove_all_favorites(db=db, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="没有收藏可清空")
    return success_response(message="清空收藏成功", data=None)

