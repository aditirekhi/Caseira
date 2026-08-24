import { HttpClient } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { map, catchError, switchMap, take, filter } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { Constants } from '../../shared/components/constants/constants';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';
import { AuthenticationService } from './authentication.service';
import { RecipeDetailReviewResponse, RecipeReviewHelpfulRequest, RecipeReviewHelpfulResponse, RecipeReviewRequest, RecipeReviewResponse } from '../../shared/interfaces/recipe-review.interface';
import { Router } from '@angular/router';

@Service()
export class ReviewsService {
    http: HttpClient = inject(HttpClient);
    router: Router = inject(Router);
    authService: AuthenticationService = inject(AuthenticationService);
    routeConstants: RouteConstants = inject(RouteConstants);
    constants: Constants = inject(Constants);

    fetchReviewsByUserId(userId: string): Observable<[] | string> {
        return this.http.get<ApiResponse<[]>>(this.routeConstants.completeFetchReviewByRecipeIdUserIdURL + `/null/${userId}`,
            { context: withTokenExpirationCheck(true) }
        )
            .pipe(
                map((response: ApiResponse<[]>): [] | string => {
                    if (response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                }
                )
            );
    }

    fetchReviewDetailsByRecipeId(recipeId: string): Observable<RecipeDetailReviewResponse | string> {
        return this.http.get<ApiResponse<RecipeDetailReviewResponse>>(`${this.routeConstants.completeFetchReviewDetailsByRecipeIdURL}/${recipeId}`)
            .pipe(
                map((response: ApiResponse<RecipeDetailReviewResponse>): RecipeDetailReviewResponse | string => {
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

    updateReview(payload: RecipeReviewRequest): Observable<RecipeReviewResponse | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.put<ApiResponse<RecipeReviewResponse>>(this.routeConstants.completeUpdateReviewURL, payload, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<RecipeReviewResponse>): RecipeReviewResponse | string => {
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
                )
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.updateReview(payload))
            );
        }
    }

    createHelpfulReview(recipeReviewId: string): Observable<RecipeReviewHelpfulResponse | string> {
        const payload: RecipeReviewHelpfulRequest = {
            recipe_review_id: recipeReviewId
        };
        if (this.authService.checkUserAuthenticated()) {
            return this.http.post<ApiResponse<RecipeReviewHelpfulResponse>>(this.routeConstants.completeCreateHelpfulReview, payload, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<RecipeReviewHelpfulResponse>): RecipeReviewHelpfulResponse | string => {
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
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$
                .pipe(
                    filter(Boolean),
                    take(1),
                    switchMap(() => this.createHelpfulReview(recipeReviewId))
                );
        }
    }

    deleteHelpfulReview(recipeReviewId: string): Observable<RecipeReviewHelpfulResponse | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.delete<ApiResponse<RecipeReviewHelpfulResponse>>(`${this.routeConstants.completeDeleteHelpfulReview}/${recipeReviewId}`, { context: withTokenExpirationCheck(true) })
                .pipe(
                    map((response: ApiResponse<RecipeReviewHelpfulResponse>): RecipeReviewHelpfulResponse | string => {
                        if (response.success) {
                            return response.data;
                        }
                        else {
                            return this.constants.GENERIC_ERROR_MESSAGE;
                        }
                    }),
                    catchError((error): Observable<string> => {
                        const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                        return of(errorMessage);
                    })
                );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$
                .pipe(
                    filter(Boolean),
                    take(1),
                    switchMap(() => this.deleteHelpfulReview(recipeReviewId))
                );
        }
    }
}