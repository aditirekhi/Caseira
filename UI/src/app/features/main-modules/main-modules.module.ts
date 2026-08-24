import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedTagsComponent } from '../../shared/components/shared-tags/shared-tags.component';
import { MainModulesRoutingModule } from './main-modules-routing.module';
import { CustomerReviewsComponent } from './customer-reviews/customer-reviews.component';
import { ExploreByRegionsComponent } from './explore-by-regions/explore-by-regions.component';
import { HeroPageComponent } from './hero-page/hero-page.component';
import { MostViewedRecipesComponent } from './most-viewed-recipes/most-viewed-recipes.component';
import { TodaysSpecialComponent } from './todays-special/todays-special.component';
import { WhyCaseiraComponent } from './why-caseira/why-caseira.component';
import { SharedButtonComponent } from '../../shared/components/shared-button/shared-button.component';
import { SharedInputComponent } from '../../shared/components/shared-input/shared-input.component';
import { SharedCustomerCardComponent } from '../../shared/components/shared-customer-card/shared-customer-card.component';
import { SharedRecipeCardComponent } from '../../shared/components/shared-recipe-card/shared-recipe-card.component';
import { SharedRegionsCardComponent } from '../../shared/components/shared-regions-card/shared-regions-card.component';


@NgModule({
  declarations: [CustomerReviewsComponent, ExploreByRegionsComponent, HeroPageComponent, MostViewedRecipesComponent, TodaysSpecialComponent, WhyCaseiraComponent],
  imports: [
    CommonModule,
    MainModulesRoutingModule,
    SharedButtonComponent,
    SharedInputComponent,
    SharedCustomerCardComponent,
    SharedRecipeCardComponent,
    SharedRegionsCardComponent,
    SharedCustomerCardComponent,
    SharedTagsComponent
  ],
  exports: [
    CustomerReviewsComponent, ExploreByRegionsComponent, HeroPageComponent, MostViewedRecipesComponent, TodaysSpecialComponent, WhyCaseiraComponent
  ]
})
export class MainModule { }
