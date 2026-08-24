import { Service } from "@angular/core";
import { environment } from "../../../../environments/environment";

@Service()

export class RouteConstants {

    public readonly baseURL: string = environment.apiUrl;

    public readonly userRoute: string = '/user';
    public readonly securityRoute: string = '/security';
    public readonly regionsRoute: string = '/regions';
    public readonly categoryRoute: string = '/category';
    public readonly recipeRoute: string = '/recipes';
    public readonly reviewsRoute: string = '/reviews';
    public readonly cartRoute: string = '/cart';
    public readonly bookmarkedFavoriteRecipe: string = '/bookmarked_favorites_recipes';
    public readonly calendarPlanDetailsRoute: string = '/user-calendar-plan-details';
    public readonly helpfulReviewRoute: string = '/helpful-reviews';

    public readonly userLogin: string = '/login';
    public readonly userSignin: string = '/signin';
    public readonly userLogout: string = '/logout'
    public readonly userForgotPassword: string = '/forgotPassword';
    public readonly checkTokenExpiration: string = '/checkTokenExpiration';
    public readonly userRefreshToken: string = '/refreshToken';
    public readonly fetchAll: string = '/all';
    public readonly todaysSpecialRecipe: string = '/todays-recipe';
    public readonly fetchDetailsById: string = '/id';
    public readonly fetchByRecipeIdUserId: string = '/byRecipeIdUserId';
    public readonly fetchByCartId: string = '/cartId';
    public readonly updateReview: string = '/update';
    public readonly fetchByUserId: string = '/userId';
    public readonly updateCartItems: string = '/update';
    public readonly deleteItemsFromCart: string = '/delete';
    public readonly favoriteRecipes: string = '/favorites';
    public readonly isFavorite: string = '/is_favorited';
    public readonly addToFavorites: string = '/addFavorite';
    public readonly deleteFromFavorites: string = '/removeFavorite';
    public readonly bookmarkedRecipes: string = '/bookmarked';
    public readonly isBookmarked: string = '/is_bookmarked';
    public readonly addToBookmarked: string = '/addBookmark';
    public readonly deleteFromBookmarked: string = '/removeBookmark';
    public readonly createPlannedDate: string = '/create';
    public readonly updatePlannedDate: string = '/update';
    public readonly createHelpfulReview: string = '/create';
    public readonly deleteHelpfulReview: string = '/delete';


    public readonly completeUserLoginURL: string = this.baseURL + this.userRoute + this.userLogin;
    public readonly completeUserSigninURL: string = this.baseURL + this.userRoute + this.userSignin;
    public readonly completeUserLogoutURL: string = this.baseURL + this.userRoute + this.userLogout;
    public readonly completeUserForgotPasswordURL: string = this.baseURL + this.userRoute + this.userForgotPassword;

    public readonly completeCheckTokenExpirationURL: string = this.baseURL + this.securityRoute + this.checkTokenExpiration;
    public readonly completeRefreshTokenURL: string = this.baseURL + this.securityRoute + this.userRefreshToken;

    public readonly completeFetchAllRegionsURL: string = this.baseURL + this.regionsRoute + this.fetchAll;

    public readonly completeFetchAllCategoriesURL: string = this.baseURL + this.categoryRoute + this.fetchAll;

    public readonly completeFetchAllRecipesCardURL: string = this.baseURL + this.recipeRoute + this.fetchAll;
    public readonly completeFetchTodaysSpecialRecipeURL: string = this.baseURL + this.recipeRoute + this.todaysSpecialRecipe;
    public readonly completeFetchRecipeDetailsByIdURL: string = this.baseURL + this.recipeRoute + this.fetchDetailsById;

    public readonly completeFetchAllReviewsURL: string = this.baseURL + this.reviewsRoute + this.fetchAll;
    public readonly completeFetchReviewDetailsByRecipeIdURL: string = this.baseURL + this.reviewsRoute + this.fetchDetailsById;
    public readonly completeFetchReviewByRecipeIdUserIdURL: string = this.baseURL + this.reviewsRoute + this.fetchByRecipeIdUserId;
    public readonly completeUpdateReviewURL: string = this.baseURL + this.reviewsRoute + this.updateReview;

    public readonly completeFetchCartByUserId: string = this.baseURL + this.cartRoute + this.fetchByUserId;
    public readonly completeUpdateCartItems: string = this.baseURL + this.cartRoute + this.updateCartItems;
    public readonly completeDeleteCartItems: string = this.baseURL + this.cartRoute + this.deleteItemsFromCart;

    public readonly completeFavoriteRecipes: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.favoriteRecipes;
    public readonly completeIsFavorite: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.isFavorite;
    public readonly completeAddToFavorites: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.addToFavorites;
    public readonly completeDeleteFromFavorites: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.deleteFromFavorites;
    public readonly completeBookmarkedRecipes: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.bookmarkedRecipes;
    public readonly completeIsBookmarked: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.isBookmarked;
    public readonly completeAddToBookmarked: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.addToBookmarked;
    public readonly completeDeleteFromBookmarked: string = this.baseURL + this.bookmarkedFavoriteRecipe + this.deleteFromBookmarked;

    public readonly completeUpdatePlannedDate: string = this.baseURL + this.calendarPlanDetailsRoute + this.updatePlannedDate;
    public readonly completeCreatePlannedDate: string = this.baseURL + this.calendarPlanDetailsRoute + this.createPlannedDate;

    public readonly completeCreateHelpfulReview: string = this.baseURL + this.helpfulReviewRoute + this.createHelpfulReview;
    public readonly completeDeleteHelpfulReview: string = this.baseURL + this.helpfulReviewRoute + this.deleteHelpfulReview;
}