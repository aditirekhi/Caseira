import { Component, DestroyRef, inject, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { filter, finalize } from 'rxjs';
import { SharedButtonComponent } from "../../../../shared/components/shared-button/shared-button.component";
import { IngredientsDetailsInterface } from '../../../../shared/interfaces/ingredients.interface';
import { RecipesService } from '../../../../core/services/recipes.service';
import { RecipeDetailsInterface } from '../../../../shared/interfaces/recipes.interface';
import { KeyValuePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CartService } from '../../../../core/services/cart.service';
import { CartDetails, UpdateCartRequest } from '../../../../shared/interfaces/cart.interface';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../../shared/components/constants/constants';

@Component({
  selector: 'app-ingredients',
  imports: [SharedButtonComponent, KeyValuePipe],
  templateUrl: './ingredients.component.html',
  styleUrl: './ingredients.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class IngredientsComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private destroyRef: DestroyRef = inject(DestroyRef);
  private constants: Constants = inject(Constants);
  private recipeService: RecipesService = inject(RecipesService);
  private cartService: CartService = inject(CartService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  recipeId: string = '';
  ingredients: Record<string, IngredientsDetailsInterface[]>[] = [];
  ingredientsInCart: string[] = [];
  quantity: number = 0;
  kitPrice: number = 0;
  ingredientsAddedToCart: boolean = false;
  addingIngredientsToCart: boolean = false;
  updatingIngredientsInCart: boolean = false;
  removingAllIngredientsFromCart: boolean = false;

  ngOnInit() {
    this.fetchRecipeDetails();
  }

  fetchRecipeDetails(): void {
    this.recipeService.recipeDetails$()
      .pipe(
        filter((response: RecipeDetailsInterface | null) => response !== null),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((response: RecipeDetailsInterface) => {
        this.recipeId = response.recipe_id;
        this.ingredients = response.ingredients;
        this.ingredientsInCart = response.recipe_ingredient_in_cart;
        this.kitPrice = response.kit_price;
        this.isRecipeInCart(this.recipeId);
        this.markIngredientsInCart(this.ingredients, this.ingredientsInCart);
        this.changeDetection.markForCheck();
      });
  }

  isRecipeInCart(recipeId: string) {
    if (this.cartService.checkRecipeExistsInCart(recipeId)) {
      this.quantity = this.cartService.fetchCartDetailsFromCookie()?.recipe_in_cart?.find(
        (item) => item.recipe_id === recipeId)?.quantity || 0;
      this.changeDetection.markForCheck();
    }
  }

  markIngredientsInCart(ingredients: Record<string, IngredientsDetailsInterface[]>[], ingredientsInCart: string[]) {
    if (this.quantity > 0) {
      for (const ingredientGroup of ingredients) {
        for (const ingredient of Object.values(ingredientGroup)) {
          for (const item of ingredient) {
            item.added_to_cart = true;
          }
        }
      }
    } else {
      for (const ingredientGroup of ingredients) {
        for (const ingredient of Object.values(ingredientGroup)) {
          for (const item of ingredient) {
            item.added_to_cart = ingredientsInCart.includes(item.ingredient_id);
            if (item.added_to_cart) {
              this.ingredientsAddedToCart = true;
            }
          }
        }
      }
    }
  }

  addRecipeToCart() {
    const payload: UpdateCartRequest = {
      recipe_in_cart: [{
        cart_id: this.cartService.fetchCartDetailsFromCookie()?.cart_id || '',
        recipe_id: this.recipeId,
        quantity: 1,
        price: this.kitPrice || 0,
      }],
      ingredients_in_cart: []
    };
    this.cartService.updateCartDetails(payload).subscribe({
      next: (response: string | CartDetails) => {
        if (typeof response === 'string') {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        } else {
          this.quantity = response.recipe_in_cart.find(item => item.recipe_id === this.recipeId)?.quantity || 0;
          this.markIngredientsInCart(this.ingredients, this.ingredientsInCart);
          this.changeDetection.markForCheck();
        }
      },
      error: (error) => {
        this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
      }
    });
  }

  private buildIngredientsCartPayload(forceRemove: boolean): UpdateCartRequest {
    const payload: UpdateCartRequest = {
      recipe_in_cart: [],
      ingredients_in_cart: []
    };

    for (const ingredientGroup of this.ingredients) {
      for (const ingredientList of Object.values(ingredientGroup)) {
        for (const item of ingredientList) {
          payload.ingredients_in_cart?.push({
            cart_id: this.cartService.fetchCartDetailsFromCookie()?.cart_id || '',
            ingredient_id: item.ingredient_id,
            quantity: !forceRemove && item.added_to_cart ? 1 : 0,
            price: item.price_per_unit,
            recipe_id: this.recipeId
          });
        }
      }
    }

    return payload;
  }

  updateIngredientInCart() {
    const isInitialAdd = !this.ingredientsAddedToCart;
    if (isInitialAdd) {
      this.addingIngredientsToCart = true;
    } else {
      this.updatingIngredientsInCart = true;
    }
    this.changeDetection.markForCheck();

    const payload = this.buildIngredientsCartPayload(false);

    this.cartService.updateCartDetails(payload)
      .pipe(
        finalize(() => {
          this.addingIngredientsToCart = false;
          this.updatingIngredientsInCart = false;
          this.changeDetection.markForCheck();
        })
      )
      .subscribe({
        next: (response: string | CartDetails) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.ingredientsAddedToCart = this.ingredients.some(ingredientGroup =>
              Object.values(ingredientGroup).some(ingredientList =>
                ingredientList.some(item => item.added_to_cart)));
          }
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  removeAllIngredientsFromCart() {
    this.removingAllIngredientsFromCart = true;
    this.changeDetection.markForCheck();

    const payload = this.buildIngredientsCartPayload(true);

    this.cartService.updateCartDetails(payload)
      .pipe(
        finalize(() => {
          this.removingAllIngredientsFromCart = false;
          this.changeDetection.markForCheck();
        })
      )
      .subscribe({
        next: (response: string | CartDetails) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            for (const ingredientGroup of this.ingredients) {
              for (const ingredientList of Object.values(ingredientGroup)) {
                for (const item of ingredientList) {
                  item.added_to_cart = false;
                }
              }
            }
            this.ingredientsAddedToCart = false;
          }
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  addRemoveIngredient(event: Event, ingredient: IngredientsDetailsInterface) {
    for (const ingredientGroup of this.ingredients) {
      for (const ingredientList of Object.values(ingredientGroup)) {
        const item = ingredientList.find(i => i.ingredient_id === ingredient.ingredient_id);
        if (item) {
          item.added_to_cart = (event.target as HTMLInputElement).checked;
          break;
        }
      }
    }
  }

  removeRecipeFromCart() {
    this.quantity = 0;
    this.markIngredientsInCart(this.ingredients, this.ingredientsInCart);
    this.changeDetection.markForCheck();
  }
}
