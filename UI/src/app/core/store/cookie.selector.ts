import { createFeatureSelector } from "@ngrx/store";
import { CookieStateInterface } from "../../shared/interfaces/generic.interface";
import { createSelector } from "@ngrx/store";

export const fetchCookieState = createFeatureSelector<CookieStateInterface>('Cookie');

export const selectCookieDetails = createSelector(
    fetchCookieState,
    (state: CookieStateInterface) => state
)