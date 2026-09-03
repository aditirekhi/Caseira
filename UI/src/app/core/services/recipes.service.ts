import { inject, Service } from '@angular/core';
import { BehaviorSubject, filter, finalize, switchMap, take } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { IsBookmarkedRecipe, IsFavoriteRecipe, RecipeAllRequestQueryParams, RecipeAllResponse, RecipeDetailsInterface, ToogleRecipeFavoriteBookmarkStatus } from '../../shared/interfaces/recipes.interface';
import { Constants } from '../../shared/components/constants/constants';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { RecipeCardInterface } from '../../shared/interfaces/recipes.interface';
import { catchError, map, Observable, of } from 'rxjs';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';
import { AuthenticationService } from './authentication.service';
import { Router } from '@angular/router';

@Service()
export class RecipesService {
    private http: HttpClient = inject(HttpClient);
    private router: Router = inject(Router);
    private constants: Constants = inject(Constants);
    private routeConstants: RouteConstants = inject(RouteConstants);
    private authService: AuthenticationService = inject(AuthenticationService);

    private recipeDetailsSubject: BehaviorSubject<RecipeDetailsInterface | null> = new BehaviorSubject<RecipeDetailsInterface | null>(null);

    recipeDetails$(): BehaviorSubject<RecipeDetailsInterface | null> {
        return this.recipeDetailsSubject;
    }

    setRecipeDetails(details: RecipeDetailsInterface | null): void {
        this.recipeDetailsSubject.next(details);
    }


    fetchAllRecipes(queryParams: RecipeAllRequestQueryParams): Observable<RecipeAllResponse | string> {
        let httpParams = new HttpParams();

        if (queryParams.order_by_field) {
            httpParams = httpParams.set('order_by_field', queryParams.order_by_field);
        }
        if (queryParams.order_by_direction) {
            httpParams = httpParams.set('order_by_direction', queryParams.order_by_direction);
        }
        if (queryParams.page_size) {
            httpParams = httpParams.set('page_size', queryParams.page_size.toString());
        }

        if (queryParams.vegetarian === true || queryParams.vegetarian === false) {
            httpParams = httpParams.set('vegetarian', queryParams.vegetarian.toString());
        }
        if (queryParams.non_vegetarian === true || queryParams.non_vegetarian === false) {
            httpParams = httpParams.set('non_vegetarian', queryParams.non_vegetarian.toString());
        }
        if (queryParams.category_id && queryParams.category_id.length > 0) {
            httpParams = httpParams.set('category_id', queryParams.category_id.join(','));
        }
        if (queryParams.region_id && queryParams.region_id.length > 0) {
            httpParams = httpParams.set('region_id', queryParams.region_id.join(','));
        }

        return this.http.get<ApiResponse<RecipeAllResponse>>(this.routeConstants.completeFetchAllRecipesCardURL,
            { params: httpParams, context: withTokenExpirationCheck(false) })
            .pipe(
                map((response: ApiResponse<RecipeAllResponse>): RecipeAllResponse | string => {
                    if (response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
    }

    fetchTodaysSpecialRecipe(): Observable<RecipeCardInterface | string> {
        return this.http.get<ApiResponse<RecipeCardInterface>>(this.routeConstants.completeFetchTodaysSpecialRecipeURL,
            { context: withTokenExpirationCheck(false) })
            .pipe(
                map((response: ApiResponse<RecipeCardInterface>): RecipeCardInterface | string => {
                    if (response.success) {
                        return response.data;
                    }
                    else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError(error => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            )
    }

    fetchRecipeDetails(recipeId: string): Observable<string> {
        this.constants.primaryLoadingPage.set(true);
        return this.http.get<ApiResponse<RecipeDetailsInterface>>(`${this.routeConstants.completeFetchRecipeDetailsByIdURL}/${recipeId}`,
            { context: withTokenExpirationCheck(false) }
        )
            .pipe(
                map((response: ApiResponse<RecipeDetailsInterface>): string => {
                    if (response.success) {
                        this.setRecipeDetails(response.data);
                        return '';
                    }
                    else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError(error => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                }),
                finalize(() => {
                    this.constants.primaryLoadingPage.set(false);
                })
            )
    }

    checkIfRecipeIsAddedToFavorites(recipeId: string): Observable<IsFavoriteRecipe | string> {
        return this.http.get<ApiResponse<IsFavoriteRecipe>>(`${this.routeConstants.completeIsFavorite}/${recipeId}`, { context: withTokenExpirationCheck(true) })
            .pipe(
                map((response: ApiResponse<IsFavoriteRecipe>) => {
                    if (response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE
                    return of(errorMessage);
                })
            )
    }

    checkIfRecipeIsBookmarked(recipeId: string): Observable<IsBookmarkedRecipe | string> {
        return this.http.get<ApiResponse<IsBookmarkedRecipe>>(`${this.routeConstants.completeIsBookmarked}/${recipeId}`, { context: withTokenExpirationCheck(true) })
            .pipe(
                map((response: ApiResponse<IsBookmarkedRecipe>): IsBookmarkedRecipe | string => {
                    if (response.success) {
                        return response.data
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE
                    return of(errorMessage);
                })
            )
    }

    addToFavorites(recipe_id: string): Observable<ToogleRecipeFavoriteBookmarkStatus | string> {
        if (this.authService.checkUserAuthenticated()) {
            const payload = {
                recipe_id
            }
            return this.http.post<ApiResponse<ToogleRecipeFavoriteBookmarkStatus>>(this.routeConstants.completeAddToFavorites, payload, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<ToogleRecipeFavoriteBookmarkStatus>): ToogleRecipeFavoriteBookmarkStatus | string => {
                        if (response.success) {
                            return response.data
                        } else {
                            return this.constants.GENERIC_ERROR_MESSAGE;
                        }
                    }),
                    catchError((error): Observable<string> => {
                        const errorMessage = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE
                        return of(errorMessage);
                    })
                );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.addToFavorites(recipe_id))
            );
        }
    }

    addToBookmarks(recipe_id: string): Observable<ToogleRecipeFavoriteBookmarkStatus | string> {
        if (this.authService.checkUserAuthenticated()) {
            const payload = {
                recipe_id
            }
            return this.http.post<ApiResponse<ToogleRecipeFavoriteBookmarkStatus>>(this.routeConstants.completeAddToBookmarked, payload, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<ToogleRecipeFavoriteBookmarkStatus>): ToogleRecipeFavoriteBookmarkStatus | string => {
                        if (response.success) {
                            return response.data
                        } else {
                            return this.constants.GENERIC_ERROR_MESSAGE
                        }
                    }),
                    catchError((error): Observable<string> => {
                        const errorMessage: string = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE;
                        return of(errorMessage);
                    })
                );
        } else {
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.addToBookmarks(recipe_id))
            );
        }
    }

    removeFromFavorites(recipe_id: string): Observable<ToogleRecipeFavoriteBookmarkStatus | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.delete<ApiResponse<ToogleRecipeFavoriteBookmarkStatus>>(`${this.routeConstants.completeDeleteFromFavorites}/${recipe_id}`, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<ToogleRecipeFavoriteBookmarkStatus>): ToogleRecipeFavoriteBookmarkStatus | string => {
                        if (response.success) {
                            return response.data
                        } else {
                            return this.constants.GENERIC_ERROR_MESSAGE;
                        }
                    }),
                    catchError((error): Observable<string> => {
                        const errorMessage = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE
                        return of(errorMessage);
                    })
                );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.removeFromFavorites(recipe_id))
            );
        }
    }

    removeFromBookmarks(recipe_id: string): Observable<ToogleRecipeFavoriteBookmarkStatus | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.delete<ApiResponse<ToogleRecipeFavoriteBookmarkStatus>>(`${this.routeConstants.completeDeleteFromBookmarked}/${recipe_id}`, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<ToogleRecipeFavoriteBookmarkStatus>): ToogleRecipeFavoriteBookmarkStatus | string => {
                        if (response.success) {
                            return response.data
                        } else {
                            return this.constants.GENERIC_ERROR_MESSAGE
                        }
                    }),
                    catchError((error): Observable<string> => {
                        const errorMessage: string = error.error?.details ?? this.constants.GENERIC_ERROR_MESSAGE;
                        return of(errorMessage);
                    })
                );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.removeFromBookmarks(recipe_id))
            );
        }
    }
}
