import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'all',
    loadComponent: () => import('./all-recipes/all-recipes.component')
      .then(m => m.AllRecipesComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./recipe-details/recipe-details.component')
      .then(m => m.RecipeDetailsComponent),
    loadChildren: () => import('./recipe-detail-sections/recipe-detail-sections.module')
      .then(m => m.RecipeDetailSectionsModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecipeRoutingModule { }
