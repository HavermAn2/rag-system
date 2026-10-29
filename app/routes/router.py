from fastapi import APIRouter
from . import documents, query

api_router = APIRouter()

api_router.include_router(documents.router)
api_router.include_router(query.query_router)
