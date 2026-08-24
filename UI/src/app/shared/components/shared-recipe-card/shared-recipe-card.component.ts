import { Component, inject, input, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { SharedButtonComponent } from "../shared-button/shared-button.component";
import { RouterModule } from '@angular/router';
import { CartService } from '../../../core/services/cart.service';
import { AuthenticationService } from '../../../core/services/authentication.service';
import { CartDetails, UpdateCartRequest } from '../../interfaces/cart.interface';
import { Constants } from '../constants/constants';
import { SharedToastNotificationService } from '../shared-toast-notification/shared-toast-notification.service';
import { RecipesService } from '../../../core/services/recipes.service';
import { IsBookmarkedRecipe, IsFavoriteRecipe, ToogleRecipeFavoriteBookmarkStatus } from '../../interfaces/recipes.interface';

@Component({
  selector: 'shared-recipe-card',
  standalone: true,
  imports: [SharedButtonComponent, RouterModule],
  templateUrl: './shared-recipe-card.component.html',
  styleUrl: './shared-recipe-card.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SharedRecipeCardComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private cartService: CartService = inject(CartService);
  private recipeService: RecipesService = inject(RecipesService);
  private authService: AuthenticationService = inject(AuthenticationService);
  private constants: Constants = inject(Constants);
  private showToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  recipeId = input<string>('');
  recipeName = input<string>('');
  kitPrice = input<number>();
  noOfPeopleServes = input<number>();
  noOfIngredients = input<number>();
  timeToCook = input<string>();
  imageUrl = input<string>('');
  cardDirection = input<'row' | 'column'>('column');
  recipeRating = input<number>(0);
  reviewCount = input<string>('');
  recipeAddedToCart = input<boolean>(false);
  recipeAddedToFavorites = input<boolean>(false);

  addToCartInProgress: boolean = false;
  addToCartSuccess: boolean = false;
  recipeInCart: boolean = false;
  cartId: string = '';
  recipeLiked: boolean = false;
  recipeBookmarked: boolean = false;
  favoriteToggleInProgress: boolean = false;
  bookmarkToggleInProgress: boolean = false;

  ngOnInit() {
    this.checkIfRecipeInCart();
    this.checkIfRecipeIsLiked();
    this.checkIfRecipeIsBookmarked();
    this.cartId = this.cartService.fetchCartDetailsFromCookie()?.cart_id || '';
  }

  getRange(num: number): number[] {
    return Array.from({ length: num }, (_, i) => i + 1);
  }

  hasHalfStar(rating: number): boolean {
    return rating % 1 !== 0;
  }

  checkIfRecipeIsLiked() {
    if (this.authService.checkUserAuthenticated()) {
      this.recipeService.checkIfRecipeIsAddedToFavorites(this.recipeId()).subscribe({
        next: (response: IsFavoriteRecipe | string) => {
          if (typeof response !== 'string') {
            this.recipeLiked = response.is_favorited;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      })
    }
  }

  checkIfRecipeIsBookmarked() {
    if (this.authService.checkUserAuthenticated()) {
      this.recipeService.checkIfRecipeIsBookmarked(this.recipeId()).subscribe({
        next: (response: IsBookmarkedRecipe | string) => {
          if (typeof response !== 'string') {
            this.recipeBookmarked = response.is_bookmarked;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
    }
  }

  checkIfRecipeInCart() {
    if (this.authService.checkUserAuthenticated() && this.cartService.checkRecipeExistsInCart(this.recipeId())) {
      this.recipeInCart = true;
      this.changeDetection.detectChanges();
    }
  }

  toggleRecipeInFavorites() {
    this.favoriteToggleInProgress = true;
    if (this.recipeLiked) {
      this.recipeService.removeFromFavorites(this.recipeId()).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          this.favoriteToggleInProgress = false;
          if (typeof response === 'string') {
            this.showToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
          } else {
            this.recipeLiked = false;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.favoriteToggleInProgress = false;
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
        }
      });
    } else if (!this.recipeLiked) {
      this.recipeService.addToFavorites(this.recipeId()).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          this.favoriteToggleInProgress = false;
          if (typeof response === 'string') {
            this.showToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
          } else {
            this.recipeLiked = true;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.favoriteToggleInProgress = false;
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
        }
      });
    }
  }

  addToCart(event: any) {
    this.addToCartInProgress = true;
    const recipePayload: UpdateCartRequest = {
      recipe_in_cart: [{
        cart_id: this.cartId,
        recipe_id: this.recipeId(),
        quantity: 1,
        price: this.kitPrice() || 0,
      }],
      ingredients_in_cart: []
    }
    this.cartService.updateCartDetails(recipePayload).subscribe({
      next: (response: string | CartDetails) => {
        if (typeof response === 'string') {
          this.showToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        } else {
          this.addToCartInProgress = false;
          this.addToCartSuccess = true;
          this.changeDetection.detectChanges();
          this.recipeInCart = true;
        }
        this.changeDetection.detectChanges();
      },
      error: (error) => {
        this.addToCartInProgress = false;
        this.showToastNotificationService.showNotification(typeof error === 'string' ? error : this.constants.GENERIC_ERROR_MESSAGE, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
      }
    });
  }

  removeRecipeFromCart() {
    this.recipeInCart = false;
    this.changeDetection.detectChanges();
  }

  toggleBookmark() {
    this.bookmarkToggleInProgress = true;
    if (this.recipeBookmarked) {
      this.recipeService.removeFromBookmarks(this.recipeId()).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          this.bookmarkToggleInProgress = false;
          if (typeof response === 'string') {
            this.showToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
          } else {
            this.recipeBookmarked = false;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.bookmarkToggleInProgress = false;
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
        }
      });
    } else {
      this.recipeService.addToBookmarks(this.recipeId()).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          this.bookmarkToggleInProgress = false;
          if (typeof response === 'string') {
            this.showToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
          } else {
            this.recipeBookmarked = true;
            this.changeDetection.detectChanges();
          }
        },
        error: (error) => {
          this.bookmarkToggleInProgress = false;
          this.showToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR'])
        }
      });
    }
  }
}