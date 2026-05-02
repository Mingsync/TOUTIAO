from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_conf import get_db
from crud.history import add_history_record, get_history_list_by_user, is_history_added, remove_history_record
from crud.history import remove_all_history as crud_remove_all_history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryAddResponse, HistoryCheckResponse, HistoryListResponces
from utils.auth import get_current_user
from utils.response import success_response



router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/check")
async def check_history(db:AsyncSession = Depends(get_db),
                        user:User = Depends(get_current_user),
                        news_id:int = Query(..., alias="newsId")):
    result = await is_history_added(db=db, user_id=user.id, news_id=news_id)
    return success_response(message="查询浏览历史状态成功", data=HistoryCheckResponse(is_viewed=result))


@router.post("/add")
async def add_history(history_request: HistoryAddRequest,
                      db:AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user),
                       ):
    result = await add_history_record(db=db, user_id=user.id, news_id=history_request.news_id)
    return success_response(message="添加浏览历史成功", data=HistoryAddResponse(history_id=result.id))


@router.delete("/remove")
async def remove_history(db:AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user),
                         news_id: int = Query(..., alias="newsId")):
    result = await remove_history_record(db=db, user_id=user.id, news_id=news_id)
    if not result:
        raise HTTPException(status_code=404, detail="浏览历史不存在")
    return success_response(message="删除浏览历史成功")

@router.get("/list")
async def get_history_list(db:AsyncSession = Depends(get_db),
                           user: User = Depends(get_current_user),
                           page: int = Query(1, ge=1, description="页码"),
                           page_size: int = Query(10, ge=1, description="每页数量")):
    stmt = await get_history_list_by_user(db=db, user_id=user.id, page=page, page_size=page_size)
    result = HistoryListResponces(list=stmt["history"], total=stmt["total"], has_more=stmt["total"] > page * page_size)
    return success_response(message="获取浏览历史列表成功", data=result)

@router.delete("/remove_all")
async def remove_all_history(db:AsyncSession = Depends(get_db),
                             user:User = Depends(get_current_user)):
    result = await crud_remove_all_history(db=db, user_id=user.id)
    if not result:
        raise HTTPException(status_code=404, detail="没有浏览历史记录可删除")
    return success_response(message="删除所有的历史浏览记录", data=None)