from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from apps.api.dependencies import get_rag_service

router = APIRouter(prefix="/rag", tags=["rag"])


class RagQueryRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=5, ge=1, le=10)


@router.post("/query")
async def query_rag(
    request: RagQueryRequest,
    service=Depends(get_rag_service),
):
    return await service.execute(request.query, top_k=request.top_k)
