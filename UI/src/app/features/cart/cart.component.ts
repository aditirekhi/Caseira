import { Component, inject } from '@angular/core';
import { NavbarComponent } from "../../core/layout/navbar/navbar.component";
import { CartService } from '../../core/services/cart.service';
import { SharedToastNotificationService } from '../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../shared/components/constants/constants';
import { CartDetails } from '../../shared/interfaces/cart.interface';

@Component({
  selector: 'app-cart',
  imports: [NavbarComponent],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.css',
})
export class CartComponent {
  private cartService: CartService = inject(CartService);
  private constants: Constants = inject(Constants);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService)

  cartDetails: CartDetails | null = null;

  ngOnInit() {
    this.fetchCartDetails();
  }

  fetchCartDetails() {
    this.cartService.fetchCartDetailsByUserId().subscribe({
      next: ((response: CartDetails | string) => {
        if (typeof response === 'string') {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        } else {
          this.cartDetails = response;
        }
      }),
      error: ((error: Error) => {
        this.sharedToastNotificationService.showNotification(this.constants.GENERIC_ERROR_MESSAGE, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
      })
    })
  }

}
