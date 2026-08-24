import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'address-details',
    loadComponent: () => import('./address-details/address-details.component')
      .then(m => m.AddressDetailsComponent)
  },
  {
    path: 'bookmarks',
    loadComponent: () => import('./bookmarked/bookmarked.component')
      .then(m => m.BookmarkedComponent)
  },
  {
    path: 'order-history',
    loadComponent: () => import('./order-history/order-history.component')
      .then(m => m.OrderHistoryComponent)
  },
  {
    path: 'payment-details',
    loadComponent: () => import('./payment-details/payment-details.component')
      .then(m => m.PaymentDetailsComponent)
  },
  {
    path: 'recipes-visited',
    loadComponent: () => import('./recipes-visited/recipes-visited.component')
      .then(m => m.RecipesVisitedComponent)
  },
  {
    path: 'reviews',
    loadComponent: () => import('./reviews/reviews.component')
      .then(m => m.ReviewsComponent)
  },
  {
    path: 'security',
    loadComponent: () => import('./security/security.component')
      .then(m => m.SecurityComponent)
  },
  {
    path: '',
    loadComponent: () => import('./overall-user-details/overall-user-details.component')
      .then(m => m.OverallUserDetailsComponent)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserDetailsRoutingModule { }
