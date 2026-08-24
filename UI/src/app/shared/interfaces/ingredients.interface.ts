export interface IngredientsDetailsInterface {
    recipe_id: string;
    recipe_item_id: string;
    ingredient_id: string;
    quantity: string;
    comment: string;
    recipe_ingredient_mapping_id: string;
    ingredient_name: string;
    price_per_unit: number;
    added_to_cart: boolean;
}
