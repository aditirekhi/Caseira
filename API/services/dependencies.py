from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import oauth2_scheme_optional_user, oauth2_scheme_user
from core.utils import decode_access_token
from database.models import UserDetails
from database.redis import is_token_blacklisted
from database.session import get_session

if TYPE_CHECKING:
    from services.address import AddressService
    from services.bookmarked_favorites_recipes import BookmarkedFavoritesRecipesService
    from services.cart import CartService
    from services.category import CategoryService
    from services.helpful_reviews import HelpfulReviewsService
    from services.ingredients import IngredientsService
    from services.recipe_review import RecipeReviewsService
    from services.recipes import RecipesService
    from services.regions import RegionsService
    from services.security import SecurityClass
    from services.user import UserService
    from services.user_calendar_plan_details import UserCalendarPlanDetailsService


databaseSessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_access_token(token: str) -> dict:
    data = decode_access_token(token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )
    token_id = data.get("jti")

    if token_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    try:
        blacklisted = await is_token_blacklisted(str(token_id))
    except RuntimeError:
        blacklisted = False

    if data is None or blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    return data


async def check_valid_request(token: Annotated[str, Depends(oauth2_scheme_user)]):
    await get_access_token(token)
    return True


async def get_user_access_token(
    token: Annotated[str, Depends(oauth2_scheme_user)],
) -> dict:
    return await get_access_token(token)


async def get_optional_user_access_token(
    token: Annotated[str | None, Depends(oauth2_scheme_optional_user)],
) -> dict | None:
    if token is None:
        return None
    return await get_access_token(token)


async def get_current_user(
    token_data: Annotated[dict, Depends(get_user_access_token)],
    databaseSession: databaseSessionDep,
) -> UserDetails:
    user_id = token_data.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    user = await databaseSession.get(UserDetails, UUID(str(user_id)))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    return user


async def get_optional_current_user(
    token_data: Annotated[dict | None, Depends(get_optional_user_access_token)],
    databaseSession: databaseSessionDep,
) -> UserDetails | None:
    if token_data is None:
        return None

    user_id = token_data.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    user = await databaseSession.get(UserDetails, UUID(str(user_id)))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    return user


def get_user_service(databaseSession: databaseSessionDep):
    from services.user import UserService

    return UserService(databaseSession)


def get_address_service(databaseSession: databaseSessionDep):
    from services.address import AddressService

    return AddressService(databaseSession)


def get_category_service(databaseSession: databaseSessionDep):
    from services.category import CategoryService

    return CategoryService(databaseSession)


def get_regions_service(databaseSession: databaseSessionDep):
    from services.regions import RegionsService

    return RegionsService(databaseSession)


def get_security_service(databaseSession: databaseSessionDep):
    from services.security import SecurityClass

    return SecurityClass(databaseSession)


def get_recipes_service(databaseSession: databaseSessionDep):
    from services.recipes import RecipesService

    return RecipesService(databaseSession)


def get_ingredient_service(databaseSession: databaseSessionDep):
    from services.ingredients import IngredientsService

    return IngredientsService(databaseSession)


def get_recipe_reviews_service(databaseSession: databaseSessionDep):
    from services.recipe_review import RecipeReviewsService

    return RecipeReviewsService(databaseSession)


def get_cart_service(databaseSession: databaseSessionDep):
    from services.cart import CartService
    from services.cart_ingredient_mapping import CartIngredientMappingService
    from services.cart_recipe_mapping import CartRecipeMappingService

    return CartService(
        databaseSession,
        cart_ingredient_mapping_service=CartIngredientMappingService(
            databaseSession, ingredient_service=get_ingredient_service(databaseSession)
        ),
        cart_recipe_mapping_service=CartRecipeMappingService(
            databaseSession, recipe_service=get_recipes_service(databaseSession)
        ),
    )


def get_bookmarked_favorites_recipes_service(databaseSession: databaseSessionDep):
    from services.bookmarked_favorites_recipes import BookmarkedFavoritesRecipesService

    return BookmarkedFavoritesRecipesService(databaseSession)


def get_user_calendar_plan_details_service(databaseSession: databaseSessionDep):
    from services.user_calendar_plan_details import UserCalendarPlanDetailsService

    return UserCalendarPlanDetailsService(databaseSession)


def get_helpful_reviews_service(databaseSession: databaseSessionDep):
    from services.helpful_reviews import HelpfulReviewsService

    return HelpfulReviewsService(databaseSession)


AddressServiceDependency = Annotated["AddressService", Depends(get_address_service)]
UserServiceDependency = Annotated["UserService", Depends(get_user_service)]
CurrentUserDependency = Annotated[UserDetails, Depends(get_current_user)]
OptionalCurrentUserDependency = Annotated[
    UserDetails | None, Depends(get_optional_current_user)
]
SecurityServiceDependency = Annotated["SecurityClass", Depends(get_security_service)]
CategoryServiceDependency = Annotated["CategoryService", Depends(get_category_service)]
RegionsServiceDependency = Annotated["RegionsService", Depends(get_regions_service)]
RecipesServiceDependency = Annotated["RecipesService", Depends(get_recipes_service)]
IngredientServiceDependency = Annotated[
    "IngredientsService", Depends(get_ingredient_service)
]
RecipeReviewsServiceDependency = Annotated[
    "RecipeReviewsService", Depends(get_recipe_reviews_service)
]
CartServiceDependency = Annotated["CartService", Depends(get_cart_service)]
BookmarkedFavoritesRecipesServiceDependency = Annotated[
    "BookmarkedFavoritesRecipesService",
    Depends(get_bookmarked_favorites_recipes_service),
]
UserCalendarPlanDetailsServiceDependency = Annotated[
    "UserCalendarPlanDetailsService", Depends(get_user_calendar_plan_details_service)
]
HelpfulReviewsServiceDependency = Annotated[
    "HelpfulReviewsService", Depends(get_helpful_reviews_service)
]
