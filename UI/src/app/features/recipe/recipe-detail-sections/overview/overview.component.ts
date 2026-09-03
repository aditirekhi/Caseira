import { ChangeDetectionStrategy, ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecipeAllRequestQueryParams, RecipeAllResponse, RecipeCardInterface, RecipeDetailsInterface } from '../../../../shared/interfaces/recipes.interface';
import { RecipeReviewRatingInput, RecipeReviewRequest, RecipeReviewResponse } from '../../../../shared/interfaces/recipe-review.interface';
import { RecipesService } from '../../../../core/services/recipes.service';
import { filter } from 'rxjs';
import { KeyValuePipe } from '@angular/common';
import { SharedTagsComponent } from '../../../../shared/components/shared-tags/shared-tags.component';
import { SharedButtonComponent } from "../../../../shared/components/shared-button/shared-button.component";
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { SharedRecipeCardComponent } from "../../../../shared/components/shared-recipe-card/shared-recipe-card.component";
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Constants } from '../../../../shared/components/constants/constants';
import { CartService } from '../../../../core/services/cart.service';
import { CartDetails, UpdateCartRequest } from '../../../../shared/interfaces/cart.interface';
import { AuthenticationRoutingModule } from "../../../../core/layout/authentication/authentication-routing.module";
import { SharedPopUpComponent } from '../../../../shared/components/shared-pop-up/shared-pop-up.component';
import { ReviewsService } from '../../../../core/services/reviews.service';

@Component({
  selector: 'app-overview',
  imports: [KeyValuePipe, FormsModule, SharedPopUpComponent, SharedTagsComponent, SharedButtonComponent, SharedRecipeCardComponent, AuthenticationRoutingModule],
  templateUrl: './overview.component.html',
  styleUrl: './overview.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OverviewComponent {
  private destroyRef: DestroyRef = inject(DestroyRef);
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private recipeService: RecipesService = inject(RecipesService);
  private cartService: CartService = inject(CartService);
  private reviewService: ReviewsService = inject(ReviewsService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  constants: Constants = inject(Constants);

  recipeDetails: RecipeDetailsInterface | null = null;
  recommendedRecipes: RecipeCardInterface[] | null = null;
  allRecipes: RecipeCardInterface[] = [];
  addingRecipeToCart: boolean = false;
  recipeInCart: boolean = false;
  showReviewPopUp: boolean = false;
  ratings: RecipeReviewRatingInput[] = [{
    index: 1,
    filled: false
  }, {
    index: 2,
    filled: false
  }, {
    index: 3,
    filled: false
  }, {
    index: 4,
    filled: false
  }, {
    index: 5,
    filled: false
  }];
  recipeComments: string = '';

  ngOnInit() {
    this.fetchRecipeDetails();
    this.fetchAllRecipeDetails();
    this.checkRecipeInCart();
  }

  checkRecipeInCart(): void {
    if (this.cartService.checkRecipeExistsInCart(this.recipeDetails?.recipe_id || '')) {
      this.recipeInCart = true;
    }
  }

  fetchRecipeDetails(): void {
    this.recipeService.recipeDetails$()
      .pipe(
        filter((response: RecipeDetailsInterface | null) => response !== null),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((response: RecipeDetailsInterface) => {
        this.recipeDetails = response;
        this.updateRecommendedRecipes();
        this.changeDetection.markForCheck();
      });
  }

  fetchAllRecipeDetails(): void {
    const payload: RecipeAllRequestQueryParams = {
      order_by_field: 'created_at',
      order_by_direction: 'desc',
      page_number: 1,
      page_size: 2
    }
    this.recipeService.fetchAllRecipes(payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response: RecipeAllResponse | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.allRecipes = response.recipes;
            this.updateRecommendedRecipes();
            this.changeDetection.markForCheck();
          }
        },
        error: (error) => {
          const errorMessage = typeof error === 'string' ? error : this.constants.GENERIC_ERROR_MESSAGE;
          this.sharedToastNotificationService.showNotification(errorMessage, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  updateRecommendedRecipes(): void {
    this.recommendedRecipes = this.allRecipes
      .filter((recipe) => recipe.recipe_id !== this.recipeDetails?.recipe_id)
      .slice(0, 1);
  }

  addRecipeToCart(): void {
    if (!this.recipeDetails || !this.recipeDetails.recipe_id || this.addingRecipeToCart) {
      return;
    }

    this.addingRecipeToCart = true;
    const payload: UpdateCartRequest = {
      recipe_in_cart: [{
        cart_id: this.cartService.fetchCartDetailsFromCookie()?.cart_id || '',
        recipe_id: this.recipeDetails.recipe_id,
        quantity: 1,
        price: this.recipeDetails.kit_price,
      }],
      ingredients_in_cart: null
    }
    this.cartService.updateCartDetails(payload)
      .subscribe({
        next: (response: CartDetails | string) => {
          this.addingRecipeToCart = false;
          this.recipeInCart = true;
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          }
          this.changeDetection.markForCheck();
        },
        error: (error) => {
          this.addingRecipeToCart = false;
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.changeDetection.markForCheck();
        }
      });
  }

  removeRecipeFromCart(): void {
    this.recipeInCart = false;
    this.changeDetection.markForCheck();
  }

  addRating(index: number): void {
    this.ratings.forEach(rating => {
      rating.filled = rating.index <= index;
    });
    this.changeDetection.markForCheck();
  }

  getRange(num: number): number[] {
    return Array.from({ length: num }, (_, i) => i + 1);
  }

  hasHalfStar(rating: number): boolean {
    return rating % 1 !== 0;
  }

  displayReviewPopUp(): void {
    this.showReviewPopUp = true;
    this.changeDetection.markForCheck();
  }

  confirmReviewPopUp(): void {
    const payload: RecipeReviewRequest = {
      ratings: this.ratings.filter(rating => rating.filled).length,
      comment: this.recipeComments,
      recipe_id: this.recipeDetails?.recipe_id || null
    };

    this.reviewService.updateReview(payload)
      .subscribe({
        next: (response: RecipeReviewResponse | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.sharedToastNotificationService.showNotification('Review submitted successfully!', this.constants.TOAST_NOTIFICATION_TYPES['SUCCESS']);
            this.recipeService.fetchRecipeDetails(this.recipeDetails?.recipe_id || '');
            this.closeReviewPopUp();
          }
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  closeReviewPopUp(): void {
    this.showReviewPopUp = false;
    this.changeDetection.markForCheck();
  }
}
