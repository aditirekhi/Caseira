export interface CartDetails {
    total_amount: number;
    cart_id: string;
    recipe_in_cart: CartRecipeMapping[];
    ingredients_in_cart: CartIngredientMapping[];
}

export interface CartRecipeMapping {
    cart_recipe_id: string;
    recipe_details: RecipeCartDetails[];
    cart_id: string;
    recipe_id: string;
    quantity: number;
    price: number;
}

export interface RecipeCartDetails {
    recipe_id: string;
    recipe_name: string;
    image_url: string;
    kit_price: number;
    vegetarian: boolean;
    category_id: string;
    region_id: string;
}

export interface CartIngredientMapping {
    cart_ingredient_id: string;
    ingredient_details: IngredientCartDetails[];
    cart_id: string;
    ingredient_id: string;
    quantity: number;
    price: number;
}

export interface IngredientCartDetails {
    ingredient_id: string;
    ingredient_name: string;
    ingredient_min_quantity: number;
    ingredient_quantity_metric: string;
    price_per_unit: number;
    image_url: string;
}

export interface UpdateCartRequest {
    recipe_in_cart: CartRecipeMappingUpdateClass[] | null;
    ingredients_in_cart: CartIngredientMappingUpdateClass[] | null;
}

export interface CartRecipeMappingUpdateClass {
    cart_id?: string;
    recipe_id: string;
    quantity: number;
    price: number;
}

export interface CartIngredientMappingUpdateClass {
    cart_id?: string;
    ingredient_id: string;
    quantity: number;
    price: number;
    recipe_id: string | null;
}

export interface CartDeleteRequest {
    cart_id: string;
    recipe_in_cart: string[] | null;
    ingredients_in_cart: string[] | null;
}