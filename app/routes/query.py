from fastapi import APIRouter,Depends
from app.dependencies import (get_query)
from app.services.query_service import Query

query_router = APIRouter()

@query_router.get("/")
async def query(users_query:str, limit = 10,query:Query = Depends(get_query) ):
    return query.request_query(users_query,limit)