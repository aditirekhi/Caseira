import { Service } from "@angular/core";
import { environment } from "../../../../environments/environment";

@Service()

export class RouteConstants {

    private readonly baseURL: string = environment.apiUrl;

    private readonly userRoute: string = '/user';
    private readonly securityRoute: string = '/security';
    private readonly regionsRoute: string = '/regions';
    private readonly categoryRoute: string = '/category';
    private readonly recipeRoute: string = '/recipes';
    private readonly reviewsRoute: string = '/reviews';
    private readonly cartRoute: string = '/cart';
    private readonly bookmarkedFavoriteRecipe: string = '/bookmarked_favorites_recipes';
    private readonly calendarPlanDetailsRoute: string = '/user-calendar-plan-details';
    private readonly helpfulReviewRoute: string = '/helpful-reviews';

    private readonly userLogin: string = '/login';
    private readonly userSignin: string = '/signin';
    private readonly userLogout: string = '/logout'
    private readonly userForgotPassword: string = '/forgotPassword';
    private readonly checkTokenExpiration: string = '/checkTokenExpiration';
    private readonly userRefreshToken: string = '/refreshToken';
    private readonly fetchAll: string = '/all';
    private readonly todaysSpecialRecipe: string = '/todays-recipe';
    private readonly fetchDetailsById: string = '/id';
    private readonly fetchByRecipeIdUserId: string = '/byRecipeIdUserId';
    private readonly fetchByCartId: string = '/cartId';
    private readonly updateReview: string = '/update';
    private readonly fetchByUserId: string = '/userId';
    private readonly updateCartItems: string = '/update';
    private readonly deleteItemsFromCart: string = '/delete';
    private readonly favoriteRecipes: string = '/favorites';
    private readonly isFavorite: string = '/is_favorited';
    private readonly addToFavorites: string = '/addFavorite';
    private readonly deleteFromFavorites: string = '/removeFavorite';
    private readonly bookmarkedRecipes: string = '/bookmarked';
    private readonly isBookmarked: string = '/is_bookmarked';
    private readonly addToBookmarked: string = '/addBookmark';
    private readonly deleteFromBookmarked: string = '/removeBookmark';
    private readonly createPlannedDate: string = '/create';
    private readonly updatePlannedDate: string = '/update';
    private readonly createHelpfulReview: string = '/create';
    private readonly deleteHelpfulReview: string = '/delete';


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