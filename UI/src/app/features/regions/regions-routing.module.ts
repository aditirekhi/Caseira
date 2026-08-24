import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'all',
    loadComponent: () => import('./all-regions/all-regions.component')
      .then(m => m.AllRegionsComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./region-details/region-details.component')
      .then(m => m.RegionDetailsComponent)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RegionsRoutingModule { }
