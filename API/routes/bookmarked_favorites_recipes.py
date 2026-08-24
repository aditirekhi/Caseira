from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.bookmarked_favorites_recipes import (
    BookmarkedFavoritesReadClass,
    BookmarkedFavoritesRecipeCreateClass,
    BookMarksFavoritesRecipeRequest,
    IsBookmarkedResponse,
    IsFavoritedResponse,
)
from schemas.recipes import RecipesClassCardRead
from services.dependencies import (
    BookmarkedFavoritesRecipesServiceDependency,
    CurrentUserDependency,
)

router = APIRouter(
    prefix="/bookmarked_favorites_recipes",
    tags=["Bookmarked Favorites Recipes"],
)


@router.get("/favorites", response_model=ApiResponse[list[RecipesClassCardRead]])
async def get_favorites_for_user(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
):
    print("---------------------------- Entering get_favorites_for_user")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    result = await bookmarked_favorites_recipes_service.get_favorites_for_user(
        currentUser.user_id
    )
    return ApiResponse(
        success=True,
        message="Favorite recipes have been fetched successfully.",
        data=result,
    )


@router.get(
    "/is_favorited/{recipe_id}", response_model=ApiResponse[IsFavoritedResponse]
)
async def is_recipe_favorited_by_user(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    recipe_id: UUID,
):
    print("---------------------------- Entering is_recipe_favorited_by_user")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    result = await bookmarked_favorites_recipes_service.is_recipe_favorited_by_user(
        currentUser.user_id, recipe_id
    )
    return ApiResponse(
        success=True,
        message="Recipe favorite status fetched successfully.",
        data=result,
    )


@router.get("/bookmarked", response_model=ApiResponse[list[RecipesClassCardRead]])
async def get_bookmarked_recipes_for_user(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
):
    print("---------------------------- Entering get_bookmarked_recipes_for_user")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    result = (
        await bookmarked_favorites_recipes_service.get_bookmarked_recipes_for__user(
            currentUser.user_id
        )
    )
    return ApiResponse(
        success=True, message="Bookmarked recipes fetched successfully", data=result
    )


@router.get(
    "/is_bookmarked/{recipe_id}", response_model=ApiResponse[IsBookmarkedResponse]
)
async def is_recipe_bookmarked_by_user(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    recipe_id: UUID,
):
    print("---------------------------- Entering is_recipe_bookmarked_by_user")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    result = await bookmarked_favorites_recipes_service.is_recipe_bookmarked_by_user(
        currentUser.user_id, recipe_id
    )
    return ApiResponse(
        message="Recipe bookmark status has been fetched successfully.",
        success=True,
        data=result,
    )


@router.post("/addFavorite", response_model=ApiResponse[BookmarkedFavoritesReadClass])
async def add_favorite(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    body: BookMarksFavoritesRecipeRequest,
):
    print("---------------------------- Entering add_favorite")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    payload = BookmarkedFavoritesRecipeCreateClass(
        recipe_id=body.recipe_id, user_id=currentUser.user_id
    )
    result = await bookmarked_favorites_recipes_service.add_favorite_for_user(
        payload, currentUser.username
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add favorite recipe for user",
        )
    return ApiResponse(
        message="Recipe added to favorites successfully",
        success=True,
        data=result,
    )


@router.post("/addBookmark", response_model=ApiResponse[BookmarkedFavoritesReadClass])
async def add_bookmark(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    body: BookMarksFavoritesRecipeRequest,
):
    print("---------------------------- Entering add_bookmark")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    payload = BookmarkedFavoritesRecipeCreateClass(
        recipe_id=body.recipe_id, user_id=currentUser.user_id
    )
    result = await bookmarked_favorites_recipes_service.add_bookmarked_recipe_for_user(
        payload, currentUser.username
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add bookmarked recipe for user",
        )
    return ApiResponse(
        message="Recipe added to bookmarks successfully",
        success=True,
        data=result,
    )


@router.delete(
    "/removeFavorite/{recipe_id}",
    response_model=ApiResponse[BookmarkedFavoritesReadClass],
)
async def remove_favorite(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    recipe_id: UUID,
):
    print("---------------------------- Entering remove_favorite")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    payload = BookmarkedFavoritesRecipeCreateClass(
        recipe_id=recipe_id, user_id=currentUser.user_id
    )
    result = await bookmarked_favorites_recipes_service.remove_favorite_for_user(
        payload
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite recipe not found for user",
        )
    return ApiResponse(
        message="Recipe removed from favorites successfully",
        success=True,
        data=result,
    )


@router.delete(
    "/removeBookmark/{recipe_id}",
    response_model=ApiResponse[BookmarkedFavoritesReadClass],
)
async def remove_bookmark(
    bookmarked_favorites_recipes_service: BookmarkedFavoritesRecipesServiceDependency,
    currentUser: CurrentUserDependency,
    recipe_id: UUID,
):
    print("---------------------------- Entering remove_bookmark")
    if not currentUser or not currentUser.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorised",
        )
    payload = BookmarkedFavoritesRecipeCreateClass(
        recipe_id=recipe_id, user_id=currentUser.user_id
    )
    result = (
        await bookmarked_favorites_recipes_service.remove_bookmarked_recipe_for_user(
            payload
        )
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmarked recipe not found for user",
        )
    return ApiResponse(
        message="Recipe removed from bookmarks successfully",
        success=True,
        data=result,
    )
