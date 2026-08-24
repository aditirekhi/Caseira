import { createReducer, on } from "@ngrx/store";
import { clearCookieState, setCookieState } from "./cookie.action";
import Cookies from 'js-cookie';
import { CookieStateInterface } from '../../shared/interfaces/generic.interface';

const APPS_COOKIE_KEY: string = 'app_persisted_state';

const cookieInitialState: CookieStateInterface = {
    cartDetails: null,
    authDetails: null
};

const getCookieInitialState = (): CookieStateInterface => {
    const cookieValue = Cookies.get(APPS_COOKIE_KEY);
    if (!cookieValue) {
        return cookieInitialState;
    }

    try {
        const parsedState = JSON.parse(cookieValue) as Partial<CookieStateInterface>;
        return {
            cartDetails: parsedState.cartDetails ?? null,
            authDetails: parsedState.authDetails ?? null
        };
    } catch {
        Cookies.remove(APPS_COOKIE_KEY);
        return cookieInitialState;
    }
};

export const cookieReducer = createReducer(
    getCookieInitialState(),
    on(setCookieState, (state, { cartDetails, authDetails }): CookieStateInterface => {
        const newState: CookieStateInterface = {
            ...state,
            cartDetails,
            authDetails
        };
        Cookies.set(APPS_COOKIE_KEY, JSON.stringify(newState));
        return newState;
    }),
    on(clearCookieState, (state): CookieStateInterface => {
        const newState: CookieStateInterface = {
            ...state,
            cartDetails: null,
            authDetails: null
        };
        Cookies.remove(APPS_COOKIE_KEY);
        return newState;
    })
);