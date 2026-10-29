from fastapi import Request
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


def get_qdrant(request: Request) -> QdrantClient:
    return request.app.state.client

def get_model(request: Request) -> SentenceTransformer:
    return request.app.state.model

def get_collection(request: Request) -> str:
    return request.app.state.collection

def get_query(request: Request):
    return request.app.state.query

def get_document(request: Request):
    return request.app.state.document