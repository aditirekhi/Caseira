import { Service, WritableSignal, signal } from "@angular/core";

@Service()

export class Constants {

    primaryLoadingPage: WritableSignal<boolean> = signal(false);
    globalScreenWidth: WritableSignal<number> = signal(window.innerWidth);


    public readonly NONE_STRING: string = 'None';

    // SignIn/Login/Forgot Password Component
    public signInLoginConstants = {
        REQUIRED_ERROR_MESSAGE: 'Please enter all the required fields.',
        EMAIL_FORMAT_ERROR_MESSAGE: 'Invalid email address provided.',
        PATTERN_VALIDATOR_ERROR_MESSAGE: 'Password does not match the constraints.',
        MIN_LENGTH_VALIDATOR_ERROR_MESSAGE: 'First and Last Name should be of minimum length of 2.',
        PASSWORD_MISMATCH_VALIDATOR_ERROR_MESSAGE: 'The passwords entered do not match.',
        POLICY_NOT_ACCEPTED_ERROR_MESSAGE: 'Policy has not been accepted.',
        PASSWORD_RESET_SUCCESS_MESSAGE: 'Password reset successful. Please login with the new password.',
        PASSWORD_RESET_FAILURE_MESSAGE: 'Password reset failed. Please check the fields and try again.',
        LOGIN_SUCCESS_MESSAGE: 'Logged in successfully.',
        LOGIN_FAILURE_MESSAGE: 'Login failed. Please check the fields and try again.'
    };

    public readonly GENERIC_ERROR_MESSAGE: string = 'An error occurred. Please try again later.';
    // Authentication Service
    public readonly CONTENT_TYPE_JSON: { 'Content-Type': string } = {
        'Content-Type': 'application/x-www-form-urlencoded'
    };

    public readonly TOAST_NOTIFICATION_TYPES: Record<string, string> = {
        'SUCCESS': 'success',
        'WARNING': 'warning',
        'ERROR': 'error'
    };

    public readonly regionsConstants = {
        UNABLE_TO_FETCH_REGIONS_ERROR_MESSAGE: 'Unable to fetch regions. Please try again later.'
    };

    public readonly SORTING_OPTIONS = {
        'ASCENDING': 'asc',
        'DESCENDING': 'desc'
    };

    public readonly recipesConstants = {
        UNABLE_TO_FETCH_RECIPES_ERROR_MESSAGE: 'Unable to fetch recipes. Please try again later.',
        RECIPE_FIELDS: {
            CATEGORY_ID: 'category_id',
            IMAGE_URL: 'image_url',
            KIT_PRICE: 'kit_price',
            NO_OF_PEOPLE_SERVED: 'no_of_people_served',
            NUMBER_OF_TOTAL_VISITS: 'number_of_total_visits',
            RECIPE_ID: 'recipe_id',
            RECIPE_NAME: 'recipe_name',
            REGION_ID: 'region_id',
            VEGETARIAN: 'vegetarian'
        },
        MOST_VIEWED_RECIPES_PAGE_SIZE: 4,
        ALL_RECIPES_PAGE_SIZE: 12
    };

    public readonly allRecipesConstants = {
        SORTING_OPTIONS: {
            'LOW_TO_HIGH': { field: 'kit_price', direction: this.SORTING_OPTIONS.ASCENDING, label: 'Low To High' },
            'HIGH_TO_LOW': { field: 'kit_price', direction: this.SORTING_OPTIONS.DESCENDING, label: 'High To Low' },
            'MOST_POPULAR': { field: 'number_of_total_visits', direction: this.SORTING_OPTIONS.DESCENDING, label: 'Most Popular' },
            'NEWEST': { field: 'created_at', direction: this.SORTING_OPTIONS.DESCENDING, label: 'Newest' },
            'CUSTOMER_REVIEWS': { field: 'rating', direction: this.SORTING_OPTIONS.DESCENDING, label: 'Customer Reviews' }
        }
    }

    private readonly skeletonTypes: string[] = ['recipe-card', 'recipe-row', 'image', 'todays-special'];

    public readonly skeletonComponentConstants = {
        SKELETON_TYPE: this.skeletonTypes
    };
}