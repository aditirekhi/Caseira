import { createAction, props } from "@ngrx/store";
import { AuthenticationResponse } from "../../shared/interfaces/authentication.interface";
import { CartDetails } from "../../shared/interfaces/cart.interface";

export const setCookieState = createAction('[Cookie] Set Cookie State', props<{ cartDetails: CartDetails | null, authDetails: AuthenticationResponse | null }>());

export const clearCookieState = createAction('[Cookie] Clear Cookie State');