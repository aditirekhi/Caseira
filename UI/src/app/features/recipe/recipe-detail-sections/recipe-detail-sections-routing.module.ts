import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'overview',
    loadComponent: () => import('./overview/overview.component')
      .then(m => m.OverviewComponent)
  },
  {
    path: 'ingredients',
    loadComponent: () => import('./ingredients/ingredients.component')
      .then(m => m.IngredientsComponent)
  },
  {
    path: 'directions',
    loadComponent: () => import('./directions/directions.component')
      .then(m => m.DirectionsComponent)
  },
  {
    path: 'nutrition',
    loadComponent: () => import('./nutrition/nutrition.component')
      .then(m => m.NutritionComponent)
  },
  {
    path: 'reviews',
    loadComponent: () => import('./reviews/reviews.component')
      .then(m => m.ReviewsComponent)
  },
  {
    path: '',
    redirectTo: 'overview',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecipeDetailSectionsRoutingModule { }
