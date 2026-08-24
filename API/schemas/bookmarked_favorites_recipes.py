from uuid import UUID

from pydantic import BaseModel


class BookmarkedFavoritesBaseClass(BaseModel):
    recipe_id: UUID
    user_id: UUID
    bookmarked: bool
    favorites: bool


class BookmarkedFavoritesReadClass(BookmarkedFavoritesBaseClass):
    pass


class BookmarkedFavoritesRecipeCreateClass(BaseModel):
    recipe_id: UUID
    user_id: UUID


class BookMarksFavoritesRecipeRequest(BaseModel):
    recipe_id: UUID


class IsBookmarkedResponse(BaseModel):
    is_bookmarked: bool


class IsFavoritedResponse(BaseModel):
    is_favorited: bool
