import { AuthenticationResponse } from "./authentication.interface";
import { CartDetails } from "./cart.interface";

export interface ApiResponse<T> {
    data: T;
    success: boolean;
    message: string;
}

export interface CookieStateInterface {
    cartDetails: CartDetails | null;
    authDetails: AuthenticationResponse | null;
}

export interface AppState {
    cookie: CookieStateInterface;
}
