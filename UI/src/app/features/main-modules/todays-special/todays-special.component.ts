import { ChangeDetectionStrategy, ChangeDetectorRef, Component, inject } from '@angular/core';
import { RecipesService } from '../../../core/services/recipes.service';
import { RecipeCardInterface } from '../../../shared/interfaces/recipes.interface';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../shared/components/constants/constants';
import { CartService } from '../../../core/services/cart.service';
import { CartDetails, UpdateCartRequest } from '../../../shared/interfaces/cart.interface';
import { AuthenticationService } from '../../../core/services/authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-todays-special',
  standalone: false,
  templateUrl: './todays-special.component.html',
  styleUrl: './todays-special.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TodaysSpecialComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private router: Router = inject(Router);
  private constants: Constants = inject(Constants);
  private recipeService: RecipesService = inject(RecipesService);
  private cartService: CartService = inject(CartService);
  private authService: AuthenticationService = inject(AuthenticationService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  todaysSpecialRecipe: RecipeCardInterface | null = null;
  addToCartInProgress: boolean = false;
  recipeAddedToCart: boolean = false;

  ngOnInit(): void {
    this.fetchTodaysSpecialRecipe();
  }

  fetchTodaysSpecialRecipe(): void {
    this.constants.primaryLoadingPage.set(true);
    this.recipeService.fetchTodaysSpecialRecipe().subscribe({
      next: (response: RecipeCardInterface | string) => {
        if (typeof response === 'string') {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        } else {
          this.todaysSpecialRecipe = response;
          this.changeDetection.detectChanges();
          this.checkIfRecipeInCart();
        }
        this.constants.primaryLoadingPage.set(false);
        this.changeDetection.detectChanges();
      },
      error: (error) => {
        const errorMessage = typeof error === 'string' ? error : this.constants.GENERIC_ERROR_MESSAGE;
        this.sharedToastNotificationService.showNotification(errorMessage, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        this.constants.primaryLoadingPage.set(false);
        this.changeDetection.detectChanges();
      }
    })
  }

  getRange(num: number): number[] {
    return Array.from({ length: num }, (_, i) => i + 1);
  }

  hasHalfStar(rating: number): boolean {
    return rating % 1 !== 0;
  }

  checkIfRecipeInCart(): void {
    if (this.authService.checkUserAuthenticated() && this.cartService.checkRecipeExistsInCart(this.todaysSpecialRecipe?.recipe_id || '')) {
      this.recipeAddedToCart = true;
      this.changeDetection.detectChanges();
    }
  }

  addToCart(recipeId: string | undefined): void {
    if (this.addToCartInProgress) {
      return;
    }

    this.addToCartInProgress = true;
    const cartDetails: UpdateCartRequest = {
      recipe_in_cart: recipeId ? [{
        recipe_id: recipeId,
        quantity: 1,
        price: this.todaysSpecialRecipe?.kit_price || 0
      }] : null,
      ingredients_in_cart: null
    }
    if (!this.authService.checkUserAuthenticated()) {
      this.authService.queuePendingRequest(this.cartService, 'updateCartDetails', cartDetails);
      this.addToCartInProgress = false;
      this.router.navigate(['/auth/login'], { queryParams: { returnUrl: this.router.url } });
      return;
    } else {
      this.cartService.updateCartDetails(cartDetails).subscribe({
        next: (response: CartDetails | string) => {
          this.addToCartInProgress = false;
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.addToCartInProgress = false;
            this.changeDetection.detectChanges();
            this.recipeAddedToCart = true;
          }
          this.changeDetection.detectChanges();
        },
        error: (error) => {
          const errorMessage = typeof error === 'string' ? error : this.constants.GENERIC_ERROR_MESSAGE;
          this.sharedToastNotificationService.showNotification(errorMessage, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.addToCartInProgress = false;
        }
      });
    }
  }

  removeRecipeFromCart() {
    this.recipeAddedToCart = false;
    this.changeDetection.detectChanges();
  }
}
