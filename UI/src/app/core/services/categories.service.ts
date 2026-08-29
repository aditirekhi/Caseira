import { Service, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { catchError, map, Observable, of } from 'rxjs';
import { AllCategoryDetailsInterface } from '../../shared/interfaces/categories.interface';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { Constants } from '../../shared/components/constants/constants';

@Service()
export class CategoriesService {
    private http: HttpClient = inject(HttpClient);
    private constants: Constants = inject(Constants);
    private routeConstants: RouteConstants = inject(RouteConstants);

    fetchAllCategories(): Observable<AllCategoryDetailsInterface[] | string> {
        return this.http.get<ApiResponse<AllCategoryDetailsInterface[]>>(this.routeConstants.completeFetchAllCategoriesURL)
            .pipe(
                map((response: ApiResponse<AllCategoryDetailsInterface[]>) => {
                    if (response.success) {
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error) => {
                    const errorMessage: string = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            )
    }
}
