import { Service } from '@angular/core';
import { AuthenticationResponse } from '../../shared/interfaces/authentication.interface';
import { AppState } from '../../shared/interfaces/generic.interface';
import { Store } from '@ngrx/store';
import { inject } from '@angular/core';
import { take } from 'rxjs';
import { clearCookieState, setCookieState } from '../store/cookie.action';
import { CartDetails } from '../../shared/interfaces/cart.interface';

@Service()
export class CookieService {
    private readonly cookieStore: Store<AppState> = inject(Store<AppState>);

    updateAuthDetailsInCookie(authDetails: AuthenticationResponse | null): void {
        this.cookieStore.select((state) => state.cookie.cartDetails)
            .pipe(take(1))
            .subscribe((cartDetails) => {
                this.cookieStore.dispatch(setCookieState({
                    cartDetails,
                    authDetails
                }));
            });
    }

    updateCartDetailsInCookie(cartDetails: CartDetails | null): void {
        this.cookieStore.select((state) => state.cookie.authDetails)
            .pipe(take(1))
            .subscribe((authDetails) => {
                this.cookieStore.dispatch(setCookieState({
                    cartDetails,
                    authDetails
                }));
            });
    }

    fetchUserAuthDetailsFromCookie(): AuthenticationResponse | null {
        let authDetails: AuthenticationResponse | null = null;
        this.cookieStore.select((state) => state.cookie.authDetails)
            .pipe(take(1))
            .subscribe((stateAuthDetails) => {
                authDetails = stateAuthDetails;
            });
        return authDetails;
    }

    fetchCartDetailsFromCookie(): CartDetails | null {
        let cartDetails: CartDetails | null = null;
        this.cookieStore.select((state) => state.cookie.cartDetails)
            .pipe(take(1))
            .subscribe((stateCartDetails) => {
                cartDetails = stateCartDetails;
            });
        return cartDetails;
    }

    clearCookieState(): void {
        this.cookieStore.dispatch(clearCookieState());
    }
}
