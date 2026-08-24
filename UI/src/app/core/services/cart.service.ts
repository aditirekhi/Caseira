import { Service, Signal, signal, WritableSignal } from '@angular/core';
import { RouteConstants } from '../../shared/components/constants/route-constants';
import { inject } from '@angular/core';
import { withTokenExpirationCheck } from '../interceptors/auth-request-context';
import { HttpClient } from '@angular/common/http';
import { catchError, finalize, map, take } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { Constants } from '../../shared/components/constants/constants';
import { CartDeleteRequest, CartDetails, CartRecipeMapping, CartRecipeMappingUpdateClass, UpdateCartRequest } from '../../shared/interfaces/cart.interface';
import { CookieService } from './cookie.service';

@Service()
export class CartService {
    private http: HttpClient = inject(HttpClient);
    private routeConstants: RouteConstants = inject(RouteConstants);
    private constants: Constants = inject(Constants);
    private cookieService: CookieService = inject(CookieService);

    fetchCartDetailsByUserId(): Observable<CartDetails | string> {
        this.constants.primaryLoadingPage.set(true);
        return this.http.get<ApiResponse<CartDetails>>(this.routeConstants.completeFetchCartByUserId,
            { context: withTokenExpirationCheck(true) }
        )
            .pipe(
                map((response: ApiResponse<CartDetails>): CartDetails | string => {
                    if (response.success) {
                        this.storeCartDetailsInCookie(response.data);
                        return response.data;
                    } else {
                        return this.constants.GENERIC_ERROR_MESSAGE;
                    }
                }),
                catchError((error): Observable<string> => {
                    const errorMessage = error.error?.detail || this.constants.GENERIC_ERROR_MESSAGE;
                    return of(errorMessage);
                }),
                finalize(() => {
                    this.constants.primaryLoadingPage.set(false);
                })
            );
    }

    updateCartDetails(payload: UpdateCartRequest): Observable<CartDetails | string> {

        const cartId = this.fetchCartDetailsFromCookie()?.cart_id;

        if (!cartId) {
            return of(this.constants.GENERIC_ERROR_MESSAGE);
        }

        const cartPayload: UpdateCartRequest = {
            recipe_in_cart: payload.recipe_in_cart?.map((item) => ({ ...item, cart_id: cartId })) ?? [],
            ingredients_in_cart: payload.ingredients_in_cart?.map((item) => ({ ...item, cart_id: cartId })) ?? []
        };

        return this.http.patch<ApiResponse<CartDetails>>(
            `${this.routeConstants.completeUpdateCartItems}/${cartId}`,
            cartPayload,
            { context: withTokenExpirationCheck(true) }
        ).pipe(
            map((response: ApiResponse<CartDetails>): CartDetails | string => {
                if (response && response.success) {
                    this.storeCartDetailsInCookie(response.data);
                    console.log('Updated cart details:', response.data);
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
    }

    deleteCartItems(payload: CartDeleteRequest): Observable<CartDetails | string> {
        return this.http.delete<ApiResponse<CartDetails>>(this.routeConstants.completeDeleteCartItems,
            { body: payload, context: withTokenExpirationCheck(true) })
            .pipe(
                map((response: ApiResponse<CartDetails>): CartDetails | string => {
                    if (response && response.success) {
                        this.storeCartDetailsInCookie(response.data);
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
    }

    fetchCartDetailsFromCookie(): CartDetails | null {
        return this.cookieService.fetchCartDetailsFromCookie();
    }

    checkRecipeExistsInCart(recipeId: string): boolean {
        const cartDetails: CartDetails | null = this.fetchCartDetailsFromCookie();
        if (cartDetails && cartDetails.recipe_in_cart) {
            return cartDetails.recipe_in_cart.some(recipe => recipe.recipe_id === recipeId);
        }
        return false;
    }

    fetchRecipeDetailsInCart(recipeId: string): CartRecipeMapping | null {
        const cartDetails: CartDetails | null = this.fetchCartDetailsFromCookie();
        if (cartDetails && cartDetails.recipe_in_cart) {
            return cartDetails.recipe_in_cart.find(recipe => recipe.recipe_id === recipeId) || null;
        }
        return null;
    }

    private storeCartDetailsInCookie(cartDetails: CartDetails | null): void {
        this.cookieService.updateCartDetailsInCookie(cartDetails);
    }
}
