import { Component } from '@angular/core';
import { RouterLinkActive, RouterLink } from '@angular/router';

@Component({
  selector: 'app-user-sidebar',
  imports: [RouterLinkActive, RouterLink],
  templateUrl: './user-sidebar.component.html',
  styleUrl: './user-sidebar.component.css',
})
export class UserSidebarComponent {
  userSidebarMenuItems = [
    { icon: 'fa-solid fa-user', name: 'Account', routerLink: 'overall-user-details' },
    { icon: 'fa-solid fa-history', name: 'Order History', routerLink: 'order-history' },
    { icon: 'fa-solid fa-bookmark', name: 'Bookmarked', routerLink: 'bookmarked' },
    { icon: 'fa-solid fa-utensils', name: 'Recipes Visited', routerLink: 'recipes-visited' },
    { icon: 'fa-solid fa-credit-card', name: 'Payment Details', routerLink: 'payment-details' },
    { icon: 'fa-solid fa-map-marker-alt', name: 'Addresses', routerLink: 'address-details' },
    { icon: 'fa-solid fa-cog', name: 'Preferences', routerLink: 'preferences' },
    { icon: 'fa-solid fa-comment', name: 'Reviews', routerLink: 'reviews' },
    { icon: 'fa-solid fa-lock', name: 'Security', routerLink: 'security' }
  ];
}
