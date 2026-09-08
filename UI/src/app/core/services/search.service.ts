import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { catchError, map, Observable, of, switchMap } from 'rxjs';
import { SearchResult } from '../../shared/interfaces/search.interface';
import { Constants } from '../../shared/components/constants/constants';
import { ApiResponse } from '../../shared/interfaces/generic.interface';

@Service()
export class SearchService {
    private http: HttpClient = inject(HttpClient);
    private constants: Constants = inject(Constants);
    private routeConstants: RouteConstants = inject(RouteConstants);

    searchRecipesIngredients(keyword: string): Observable<SearchResult[] | string> {
        const params: HttpParams = new HttpParams().set('keyword', keyword);
        return this.http.get<ApiResponse<SearchResult[]>>(this.routeConstants.completeSearchURL, { params })
            .pipe(
                map((response: ApiResponse<SearchResult[]>): SearchResult[] | string => {
                    return response.data ?? [];
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail ?? this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                })
            );
    }
}