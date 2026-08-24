import { inject, Service } from '@angular/core';
import { AuthenticationService } from './authentication.service';
import { Router } from '@angular/router';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { HttpClient } from '@angular/common/http';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';
import { UserCalendarPlanDetailsRead, UserCalendarPlanDetailsCreateUpdate } from '../../shared/interfaces/user-calendar-plan-details';
import { catchError, filter, map, Observable, of, switchMap, take } from 'rxjs';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { Constants } from '../../shared/components/constants/constants';

@Service()
export class CalendarPlanDetailsService {
    private http: HttpClient = inject(HttpClient);
    private router: Router = inject(Router);
    private authService: AuthenticationService = inject(AuthenticationService);
    private routeConstant: RouteConstants = inject(RouteConstants);
    private constants: Constants = inject(Constants);

    updatePlannedDate(payload: UserCalendarPlanDetailsCreateUpdate): Observable<UserCalendarPlanDetailsRead | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.put<ApiResponse<UserCalendarPlanDetailsRead>>(
                this.routeConstant.completeUpdatePlannedDate,
                payload, {
                context: withTokenExpirationCheck(true)
            }
            ).pipe(
                map((response: ApiResponse<UserCalendarPlanDetailsRead>): UserCalendarPlanDetailsRead | string => {
                    if (response && response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail || this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.updatePlannedDate(payload))
            );
        }
    }

    createPlannedDate(payload: UserCalendarPlanDetailsCreateUpdate): Observable<UserCalendarPlanDetailsRead | string> {
        if (this.authService.checkUserAuthenticated()) {
            return this.http.post<ApiResponse<UserCalendarPlanDetailsRead>>(
                this.routeConstant.completeCreatePlannedDate,
                payload, {
                context: withTokenExpirationCheck(true)
            }
            ).pipe(
                map((response: ApiResponse<UserCalendarPlanDetailsRead>): UserCalendarPlanDetailsRead | string => {
                    if (response && response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail || this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
        } else {
            this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
            return this.authService.isWorkflowComplete$.pipe(
                filter(Boolean),
                take(1),
                switchMap(() => this.createPlannedDate(payload))
            );
        }
    }
}
