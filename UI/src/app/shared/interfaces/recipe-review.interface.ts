export interface RecipeReviewRatingInput {
    index: number;
    filled: boolean;
}

export interface RecipeReviewRequest {
    ratings: number | null;
    comment: string | null;
    recipe_id: string | null;
}

export interface RecipeReviewResponse {
    recipe_review_id: string;
    ratings: number | null;
    comment: string | null;
    user_id: string;
    recipe_id: string;
    username: string;
    created_at: string;
    helpful_review_count: number;
    helpful_review_given_by_user: boolean;
}

export interface RecipeDetailReviewResponse {
    total_review_count: number;
    review_count_5: number;
    review_count_4: number;
    review_count_3: number;
    review_count_2: number;
    review_count_1: number;
    avg_rating: number;
    review_details: RecipeReviewResponse[];
}

export interface RecipeReviewHelpfulRequest {
    recipe_review_id: string;
}

export interface RecipeReviewHelpfulResponse {
    helpful_review_id: string;
    user_id: string;
    recipe_review_id: string;
}

export type TimeUnit = 'year' | 'month' | 'day' | 'hour' | 'minute' | 'second';
