import { Component, ChangeDetectionStrategy, input, output, inject, model, ChangeDetectorRef, SimpleChanges } from '@angular/core';
import { CookieService } from '../../../core/services/cookie.service';
import { finalize } from 'rxjs';
import { CartService } from '../../../core/services/cart.service';
import { CartDetails, CartIngredientMapping, CartRecipeMapping, UpdateCartRequest } from '../../interfaces/cart.interface';
import { SharedToastNotificationService } from '../shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../constants/constants';

@Component({
  selector: 'shared-button',
  standalone: true,
  imports: [],
  templateUrl: './shared-button.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    '[style.width]': 'buttonWidth() || null'
  },
  styleUrl: './shared-button.component.css'
})
export class SharedButtonComponent {
  private changeDetection = inject(ChangeDetectorRef);
  private constants: Constants = inject(Constants);
  private cartService: CartService = inject(CartService);
  private cookieService = inject(CookieService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  buttonClass = input<string>('');
  buttonType = input<'button' | 'submit' | 'reset'>('button');
  iconOnly = input<boolean>(false);
  addIcon = input<boolean>(false);
  iconClass = input<string>('');
  rightIconClass = input<string>('');
  leftIcon = input<boolean>(false);
  addLeftRightIcons = input<boolean>(false);
  buttonWidth = input<string>('');
  disabled = input<boolean>(false);
  addedToCartButton = input<boolean>(false);
  itemId = input<string | undefined>('');

  recipeDeleted = output<boolean>();

  quantity: string = '0';

  addingReducingItemFromCart: boolean = false;

  ngOnChanges(changes: SimpleChanges) {
    console.log('Initializing SharedButtonComponent with itemId:', this.itemId());
    if (this.addedToCartButton() && this.itemId()) {
      console.log('Cart details from cookie:', this.cookieService.fetchCartDetailsFromCookie());
      // this.quantity = String(this.cartService.fetchRecipeDetailsInCart(this.itemId() || '')?.quantity || '0');
      this.quantity = String(this.cookieService.fetchCartDetailsFromCookie()?.recipe_in_cart
        .find(recipe => recipe.recipe_id === this.itemId())?.quantity ||
        this.cookieService.fetchCartDetailsFromCookie()?.ingredients_in_cart
          .find(ingredient => ingredient.ingredient_id === this.itemId())?.quantity || '0');
    }
  }

  addItem() {
    const itemDetails = this.cookieService.fetchCartDetailsFromCookie()?.recipe_in_cart
      .find(recipe => recipe.recipe_id === this.itemId()) ||
      this.cookieService.fetchCartDetailsFromCookie()?.ingredients_in_cart
        .find(ingredient => ingredient.ingredient_id === this.itemId());
    if (itemDetails) {
      this.addingReducingItemFromCart = true;
      const payload: UpdateCartRequest = 'cart_ingredient_id' in itemDetails
        ? {
          recipe_in_cart: null,
          ingredients_in_cart: [{
            cart_id: itemDetails.cart_id,
            ingredient_id: itemDetails.ingredient_id,
            quantity: itemDetails.quantity + 1,
            price: itemDetails.price,
            recipe_id: itemDetails.recipe_id
          }]
        }
        : {
          recipe_in_cart: [{
            cart_id: itemDetails.cart_id,
            recipe_id: itemDetails.recipe_id,
            quantity: itemDetails.quantity + 1,
            price: itemDetails.price
          }],
          ingredients_in_cart: null
        };
      this.cartService.updateCartDetails(payload)
        .pipe(
          finalize(() => {
            this.addingReducingItemFromCart = false;
            this.changeDetection.markForCheck();
          })
        )
        .subscribe({
          next: (response: CartDetails | string) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.quantity = String(response.recipe_in_cart.find(recipe => recipe.recipe_id === this.itemId())?.quantity ||
                String(response.ingredients_in_cart.find(ingredient => ingredient.ingredient_id === this.itemId())?.quantity) || 0);
              if (this.quantity === '0') {
                this.recipeDeleted.emit(true);
              }
            }
          },
          error: () => {
            this.sharedToastNotificationService.showNotification(this.constants.GENERIC_ERROR_MESSAGE, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          }
        });
    }
  }

  reduceItem() {
    const itemDetails = this.cookieService.fetchCartDetailsFromCookie()?.recipe_in_cart
      .find(recipe => recipe.recipe_id === this.itemId()) || this.cookieService.fetchCartDetailsFromCookie()?.ingredients_in_cart
        .find(ingredient => ingredient.ingredient_id === this.itemId());

    if (itemDetails && itemDetails.quantity > 0) {
      const updateRequest: UpdateCartRequest = 'cart_ingredient_id' in itemDetails
        ? {
          recipe_in_cart: null,
          ingredients_in_cart: [{
            cart_id: itemDetails.cart_id,
            ingredient_id: itemDetails.ingredient_id,
            quantity: itemDetails.quantity - 1,
            price: itemDetails.price,
            recipe_id: itemDetails.recipe_id
          }]
        }
        : {
          recipe_in_cart: [{
            cart_id: itemDetails.cart_id,
            recipe_id: itemDetails.recipe_id,
            quantity: itemDetails.quantity - 1,
            price: itemDetails.price
          }],
          ingredients_in_cart: null
        };
      this.addingReducingItemFromCart = true;
      this.cartService.updateCartDetails(updateRequest)
        .pipe(
          finalize(() => {
            this.addingReducingItemFromCart = false;
            this.changeDetection.markForCheck();
          })
        )
        .subscribe({
          next: (response: CartDetails | string) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.quantity = String(response.recipe_in_cart.find(recipe => recipe.recipe_id === this.itemId())?.quantity ||
                String(response.ingredients_in_cart.find(ingredient => ingredient.ingredient_id === this.itemId())?.quantity) || 0);
              if (this.quantity === '0') {
                this.recipeDeleted.emit(true);
              }
            }
          },
          error: () => {
            this.sharedToastNotificationService.showNotification(this.constants.GENERIC_ERROR_MESSAGE, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          }
        });
    }
  }
}
