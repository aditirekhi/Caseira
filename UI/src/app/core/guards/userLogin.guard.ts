import { CanActivateFn, Router } from "@angular/router";
import { AuthenticationService } from "../services/authentication.service";
import { inject } from "@angular/core";
import { map, of, switchMap, take } from "rxjs";

export const checkUserLogin: CanActivateFn = (route, state) => {
    const authService: AuthenticationService = inject(AuthenticationService);
    const router = inject(Router);

    const redirectToLogin = () => router.createUrlTree(['/auth/login'], {
        queryParams: { returnUrl: state.url }
    });

    return authService.isWorkflowComplete$.pipe(
        take(1),
        switchMap((isWorkflowComplete: boolean) => {
            if (isWorkflowComplete) {
                return of(true);
            }
            // in-memory flag resets on reload, so fall back to validating the cookie token
            if (!authService.checkUserAuthenticated()) {
                return of(redirectToLogin());
            }
            return authService.checkTokenExpiration().pipe(
                take(1),
                map((isTokenExpired: boolean) => isTokenExpired ? redirectToLogin() : true)
            );
        })
    );
}