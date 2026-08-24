import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from './cookie.service';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { AuthenticationResponse, ChangePasswordRequest, UserLogInRequest, UserSignInRequest } from '../../shared/interfaces/authentication.interface';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { Constants } from '../../shared/components/constants/constants';
import { BehaviorSubject, catchError, map, Observable, of, switchMap } from 'rxjs';
import { UpdateCartRequest } from '../../shared/interfaces/cart.interface';
import { CartService } from './cart.service';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';

@Service()
export class AuthenticationService {
    private http: HttpClient = inject(HttpClient);
    private router: Router = inject(Router);
    private cookieService: CookieService = inject(CookieService);
    private routeConstant: RouteConstants = inject(RouteConstants);
    private cartService: CartService = inject(CartService);
    private constants: Constants = inject(Constants);

    private workflowComplete$ = new BehaviorSubject<boolean>(false);

    private pendingRequestQueue: { service: CartService, method: string, payload: UpdateCartRequest }[] = [];

    get isWorkflowComplete$(): Observable<boolean> {
        return this.workflowComplete$.asObservable();
    }

    setWorkflowComplete(value: boolean): void {
        this.workflowComplete$.next(value);
    }

    userSignIn(userSignInPayload: UserSignInRequest): Observable<string | null> {
        return this.http.post<ApiResponse<AuthenticationResponse>>(
            this.routeConstant.completeUserSigninURL,
            userSignInPayload,
            { context: withTokenExpirationCheck(false) }
        )
            .pipe(
                switchMap((response) => {
                    if (response.success) {
                        if (response.data.access_token) {
                            this.storeToken(response.data);
                            this.setWorkflowComplete(true);
                            this.cartService.fetchCartDetailsByUserId().subscribe();
                            return of(null);
                        } else {
                            return of(this.constants.GENERIC_ERROR_MESSAGE);
                        }
                    }
                    return of(this.constants.GENERIC_ERROR_MESSAGE);
                }),
                catchError((error: HttpErrorResponse): Observable<string> => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
    }

    userLogin(userLoginPayload: UserLogInRequest): Observable<string | null> {
        const payload = new HttpParams()
            .set('username', userLoginPayload.username,)
            .set('password', userLoginPayload.password);

        const headers = new HttpHeaders(this.constants.CONTENT_TYPE_JSON);

        return this.http.post<ApiResponse<AuthenticationResponse>>(
            this.routeConstant.completeUserLoginURL,
            payload.toString(), { headers, context: withTokenExpirationCheck(false) })
            .pipe(
                switchMap((response) => {
                    if (response.success) {
                        if (response.data.access_token) {
                            this.storeToken(response.data);
                            this.setWorkflowComplete(true);
                            this.cartService.fetchCartDetailsByUserId().subscribe();
                            return of(null);
                        } else {
                            return of(this.constants.GENERIC_ERROR_MESSAGE);
                        }
                    }
                    return of(this.constants.GENERIC_ERROR_MESSAGE);
                }),
                catchError((error: HttpErrorResponse): Observable<string> => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
    }

    userLogout() {

    }

    userForgotPassword(request: ChangePasswordRequest): Observable<string | null> {
        return this.http.post<ApiResponse<null>>(
            this.routeConstant.completeUserForgotPasswordURL,
            request,
            { context: withTokenExpirationCheck(false) }
        ).pipe(
            map((response: ApiResponse<null>): string | null => {
                if (response.success) {
                    return null;
                } else {
                    return this.constants.signInLoginConstants.PASSWORD_RESET_FAILURE_MESSAGE;
                }
            }),
            catchError((error: HttpErrorResponse): Observable<string> => {
                const errorMessage = error.error?.detail ?? this.constants.signInLoginConstants.PASSWORD_RESET_FAILURE_MESSAGE;
                return of(errorMessage);
            })
        );
    }

    checkTokenExpiration(): Observable<boolean> {
        return this.http.get<ApiResponse<boolean>>(this.routeConstant.completeCheckTokenExpirationURL,
            { context: withTokenExpirationCheck(false) }
        )
            .pipe(
                map((response: ApiResponse<boolean>): boolean => {
                    if (response.success && response.data) {
                        this.setWorkflowComplete(!response.data);
                        return response.data;
                    } else {
                        return false;
                    }
                }),
                catchError((error: HttpErrorResponse): Observable<boolean> => {
                    this.setWorkflowComplete(false);
                    return of(true);
                })
            );
    }

    refreshToken(): Observable<AuthenticationResponse | null> {
        return this.http.post<ApiResponse<AuthenticationResponse>>(this.routeConstant.completeRefreshTokenURL,
            { context: withTokenExpirationCheck(false) })
            .pipe(
                map((response: ApiResponse<AuthenticationResponse>): AuthenticationResponse | null => {
                    if (response.success) {
                        if (response.data.access_token) {
                            this.setWorkflowComplete(true);
                            this.storeToken(response.data);
                            return response.data;
                        }
                        this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
                        this.setWorkflowComplete(false);
                        return null;
                    } else {
                        this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
                        this.setWorkflowComplete(false);
                        return null;
                    }
                }),
                catchError((): Observable<AuthenticationResponse | null> => {
                    this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
                    this.setWorkflowComplete(false);
                    return of(null);
                })
            );
    }

    checkUserAuthenticated(): boolean {
        const authDetails = this.cookieService.fetchUserAuthDetailsFromCookie();
        if (authDetails && authDetails.access_token) {
            return true;
        } else {
            return false;
        }
    }

    hasPendingRequests(): boolean {
        return this.pendingRequestQueue.length > 0;
    }

    queuePendingRequest(service: CartService, method: string, payload: UpdateCartRequest) {
        this.pendingRequestQueue.push({ service, method, payload });
    }

    processPendingRequests() {
        while (this.pendingRequestQueue.length > 0) {
            const { service, method, payload } = this.pendingRequestQueue.shift()!;
            const request = (service as any)[method](payload);
            if (request && typeof request.subscribe === 'function') {
                request.subscribe();
            }
        }
    }

    private storeToken(token_data: AuthenticationResponse) {
        this.cookieService.updateAuthDetailsInCookie(token_data);
    }
}
