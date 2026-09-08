from fastapi import APIRouter

from schemas.base import ApiResponse
from schemas.search import SearchResult
from services.dependencies import SearchServiceDependency

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=ApiResponse[list[SearchResult]])
async def search_recipes_ingredients(
    keyword: str, search_service: SearchServiceDependency, limit: int = 10
):
    print("-------------------------------- Entering search_recipes_ingredients")

    return ApiResponse(
        success=True,
        data=await search_service.search_recipes_ingredients(keyword, limit),
        message="Search completed successfully",
    )
