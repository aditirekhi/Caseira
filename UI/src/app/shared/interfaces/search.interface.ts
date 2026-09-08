export interface SearchResult {
    recipe_id: string;
    recipe_name: string;
    ingredient_list: [{
        ingredient_id: string;
        ingredient_name: string;
    }];
}