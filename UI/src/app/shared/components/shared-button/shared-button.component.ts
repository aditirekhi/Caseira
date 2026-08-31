import { Component, ChangeDetectionStrategy, input, output, inject, model, ChangeDetectorRef } from '@angular/core';
import { finalize } from 'rxjs';
import { CartService } from '../../../core/services/cart.service';
import { CartDetails, UpdateCartRequest } from '../../interfaces/cart.interface';
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
  recipeId = input<string | undefined>('');

  recipeDeleted = output<boolean>();

  quantity: string = '0';

  addingReducingItemFromCart: boolean = false;

  ngOnInit() {
    if (this.addedToCartButton() && this.recipeId()) {
      this.quantity = String(this.cartService.fetchRecipeDetailsInCart(this.recipeId() || '')?.quantity || 0);
    }
  }

  addItem() {
    const recipeDetails = this.cartService.fetchRecipeDetailsInCart(this.recipeId() || '');
    if (recipeDetails) {
      this.addingReducingItemFromCart = true;
      const payload: UpdateCartRequest = {
        recipe_in_cart: [{
          cart_id: recipeDetails.cart_id,
          recipe_id: recipeDetails.recipe_id,
          quantity: recipeDetails.quantity + 1,
          price: recipeDetails.price
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
              this.quantity = String(response.recipe_in_cart.find(recipe => recipe.recipe_id === this.recipeId())?.quantity || 0);
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
    const recipeDetails = this.cartService.fetchRecipeDetailsInCart(this.recipeId() || '');
    if (recipeDetails && recipeDetails.quantity > 0) {
      const updateRequest: UpdateCartRequest = {
        recipe_in_cart: [{
          cart_id: recipeDetails.cart_id,
          recipe_id: recipeDetails.recipe_id,
          quantity: recipeDetails.quantity - 1,
          price: recipeDetails.price
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
              this.quantity = String(response.recipe_in_cart.find(recipe => recipe.recipe_id === this.recipeId())?.quantity || 0);
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
