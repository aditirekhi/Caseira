import { CanActivateFn, Router } from "@angular/router";
import { AuthenticationService } from "../services/authentication.service";
import { inject } from "@angular/core";
import { map, take } from "rxjs";

export const checkUserLogin: CanActivateFn = (route, state) => {
    const authService: AuthenticationService = inject(AuthenticationService);
    const router = inject(Router);

    return authService.isWorkflowComplete$.pipe(
        take(1),
        map((isWorkflowComplete: boolean) => {
            if (isWorkflowComplete) {
                return true;
            }
            return router.createUrlTree(['/auth/login'], {
                queryParams: { returnUrl: state.url }
            });
        })
    );
}