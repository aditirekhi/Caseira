import { inject, Service } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { FetchAllRegionsResponse } from '../../shared/interfaces/regions.interface';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { catchError, map, Observable } from 'rxjs';
import { Constants } from '../../shared/components/constants/constants';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';

@Service()
export class RegionsService {
    private http = inject(HttpClient);
    private routeConstant: RouteConstants = inject(RouteConstants);
    private constants: Constants = inject(Constants);

    getAllRegions(): Observable<FetchAllRegionsResponse[] | string> {
        return this.http.get<ApiResponse<FetchAllRegionsResponse[]>>(this.routeConstant.completeFetchAllRegionsURL,
            { context: withTokenExpirationCheck(false) }
        )
            .pipe(
                map((response: ApiResponse<FetchAllRegionsResponse[]>): FetchAllRegionsResponse[] | string => {
                    if (response.success) {
                        return response.data;
                    } else {
                        return response.message || this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error: HttpErrorResponse): string => {
                    return error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                })
            );
    }
}
