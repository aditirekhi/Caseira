import { ChangeDetectionStrategy, ChangeDetectorRef, Component, inject } from '@angular/core';
import { SharedToastNotificationService } from '../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../shared/components/constants/constants';
import { CartDetails } from '../../shared/interfaces/cart.interface';
import { CookieService } from '../../core/services/cookie.service';
import { SharedButtonComponent } from '../../shared/components/shared-button/shared-button.component';
import { SharedTagsComponent } from '../../shared/components/shared-tags/shared-tags.component';

@Component({
  selector: 'app-cart',
  imports: [SharedButtonComponent, SharedTagsComponent],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CartComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private cookieService: CookieService = inject(CookieService);
  private constants: Constants = inject(Constants);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  cartDetails: CartDetails | null = null;
  totalItems: number = 0;
  totalPrice: number = 0;

  ngOnInit() {
    this.fetchCartDetails();
  }

  fetchCartDetails() {
    this.cartDetails = this.cookieService.fetchCartDetailsFromCookie();
    if (this.cartDetails) {
      this.totalItems = this.cartDetails.ingredients_in_cart.length + this.cartDetails.recipe_in_cart.length;
      this.totalPrice = this.calculateTotalPrice(this.cartDetails);
    }
    this.changeDetection.markForCheck();
  }

  calculateTotalPrice(cartDetails: CartDetails): number {
    let totalPrice = 0;
    for (const cartItem of cartDetails.ingredients_in_cart) {
      totalPrice += cartItem.price * cartItem.quantity;
    }
    for (const cartItem of cartDetails.recipe_in_cart) {
      totalPrice += cartItem.price * cartItem.quantity;
    }
    return totalPrice;
  }

}
