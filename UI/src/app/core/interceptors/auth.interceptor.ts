import { HttpHandlerFn, HttpInterceptorFn, HttpRequest } from "@angular/common/http";
import { inject } from "@angular/core";
import { catchError, of, switchMap, take } from "rxjs";
import { CookieService } from "../services/cookie.service";
import { RouteConstants } from "../../shared/components/constants/route-constants";
import { AuthenticationService } from "../services/authentication.service";
import { AuthenticationResponse } from "../../shared/interfaces/authentication.interface";
import { SHOULD_CHECK_TOKEN_EXPIRATION } from "./auth-request-context";

export const authInterceptor: HttpInterceptorFn = (
    req: HttpRequest<unknown>,
    next: HttpHandlerFn
) => {
    const cookieService: CookieService = inject(CookieService);
    const authService: AuthenticationService = inject(AuthenticationService);
    const routeConstant = inject(RouteConstants);

    if (req.url.includes(routeConstant.completeUserLoginURL) || req.url.includes(routeConstant.completeUserSigninURL)) {
        return next(req);
    }

    const currentAuthDetails = cookieService.fetchUserAuthDetailsFromCookie();
    if (!currentAuthDetails?.access_token) {
        return next(req);
    }

    const createAuthorizedRequest = (
        request: HttpRequest<unknown>,
        authDetails: AuthenticationResponse
    ): HttpRequest<unknown> => {
        const tokenType = authDetails.token_type || 'Bearer';
        return request.clone({
            setHeaders: {
                Authorization: `${tokenType} ${authDetails.access_token}`,
            }
        });
    };

    const requestWithCurrentToken = createAuthorizedRequest(req, currentAuthDetails);
    const shouldCheckTokenExpiration = req.context.get(SHOULD_CHECK_TOKEN_EXPIRATION);

    if (
        !shouldCheckTokenExpiration
        ||
        req.url.includes(routeConstant.completeCheckTokenExpirationURL)
        || req.url.includes(routeConstant.completeRefreshTokenURL)
    ) {
        return next(requestWithCurrentToken);
    }

    return authService.checkTokenExpiration().pipe(
        take(1),
        switchMap((isTokenExpired: boolean) => {
            if (!isTokenExpired) {
                return next(requestWithCurrentToken);
            }

            return authService.refreshToken().pipe(
                take(1),
                switchMap((refreshedAuthDetails: AuthenticationResponse | null) => {
                    const latestAuthDetails = refreshedAuthDetails ?? cookieService.fetchUserAuthDetailsFromCookie();
                    if (!latestAuthDetails?.access_token) {
                        return next(req);
                    }
                    return next(createAuthorizedRequest(req, latestAuthDetails));
                })
            );
        }),
        catchError(() => next(requestWithCurrentToken))
    );
};