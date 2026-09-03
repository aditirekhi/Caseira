import { IngredientsDetailsInterface } from "./ingredients.interface";

export interface RecipeAllRequestQueryParams {
    order_by_field?: string;
    order_by_direction?: string;
    page_size?: number;
    category_id?: string[];
    region_id?: string[];
    vegetarian?: boolean;
    non_vegetarian?: boolean;
}

export interface RecipeAllResponse {
    recipes: RecipeCardInterface[];
    total_recipe: number;
}

export interface RecipeCardInterface {
    recipe_name: string;
    image_url: string;
    number_of_total_visits: number;
    kit_price: number;
    no_of_people_served: number;
    vegetarian: boolean;
    total_time: string;
    ratings: number;
    recipe_description: string;
    recipe_id: string;
    category_id: string;
    region_id: string;
    ingredients_count: number;
    review_count: string;
}

export interface RecipeItemsInterface {
    recipe_item_id: string;
    item_name: string;
    item_description: string;

}

export interface RecipeDetailsInterface {
    recipe_name: string;
    image_url: string;
    number_of_total_visits: number;
    kit_price: number;
    no_of_people_served: number;
    vegetarian: boolean;
    total_time: string;
    ratings: number;
    recipe_description: string;
    recipe_id: string;
    category_name: string;
    region_name: string;
    recipe_items: RecipeItemsInterface[];
    recipe_directions: Record<string, string[]>;
    nutrition_details: Record<string, string>[];
    ingredients: Record<string, IngredientsDetailsInterface[]>[];
    recipe_ingredient_in_cart: string[];
    prep_time: string;
    cook_time: string;
    difficulty_level: string;
    features: string[];
    review_count: string;
    plan_date: string | null;
    is_bookmarked: boolean;
    is_favorited: boolean;
}

export interface IsFavoriteRecipe {
    is_favorited: boolean
}

export interface IsBookmarkedRecipe {
    is_bookmarked: boolean
}

export interface ToogleRecipeFavoriteBookmarkStatus {
    recipe_id: string;
    user_id: string;
    bookmarked: boolean;
    favorite: boolean;
}

export interface SortingOptions {
    field: string;
    direction: string;
    label: string;
}