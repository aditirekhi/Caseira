import { Routes } from '@angular/router';
import { checkUserLogin } from './core/guards/userLogin.guard';

export const routes: Routes = [
    {
        path: 'recipe',
        loadChildren: () => import('./features/recipe/recipe.module')
            .then(m => m.RecipeModule)
    },
    {
        path: 'user-profile',
        loadChildren: () => import('./features/user-details/user-details.module')
            .then(m => m.UserDetailsModule),
        canActivate: [checkUserLogin]
    },
    {
        path: 'cart',
        loadComponent: () => import('./features/cart/cart.component')
            .then(m => m.CartComponent),
        canActivate: [checkUserLogin]
    },
    {
        path: 'auth',
        loadChildren: () => import('./core/layout/authentication/authentication.module')
            .then(m => m.AuthenticationModule)
    },
    {
        path: 'home',
        loadChildren: () => import('./features/main-modules/main-modules.module')
            .then(m => m.MainModule)
    },
    {
        path: 'ingredients',
        loadComponent: () => import('./features/all-ingredients/all-ingredients.component')
            .then(m => m.AllIngredientsComponent)
    },
    {
        path: 'meal-kits',
        loadComponent: () => import('./features/meal-kits/meal-kits.component')
            .then(m => m.MealKitsComponent)
    },
    {
        path: 'regions',
        loadChildren: () => import('./features/regions/regions.module')
            .then(m => m.RegionsModule)
    },
    {
        path: '**',
        redirectTo: 'home'
    }
];
