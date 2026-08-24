import { APP_INITIALIZER, ApplicationConfig, inject, provideAppInitializer, provideZoneChangeDetection } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideStore } from '@ngrx/store';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { cookieReducer } from './core/store/cookie.reducer';
import { CartService } from './core/services/cart.service';
import { SharedToastNotificationService } from './shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from './shared/components/constants/constants';
import { of } from 'rxjs';

function initializeApp() {
  const cartService: CartService = inject(CartService);
  const sharedToastNotificationService = inject(SharedToastNotificationService);
  const constants: Constants = inject(Constants);

  cartService.fetchCartDetailsByUserId().subscribe({
    next: (response) => {
      return of(null);
    },
    error: (error) => {
      return of(null);
    }
  });


}

export const appConfig: ApplicationConfig = {
  providers: [
    provideAppInitializer(initializeApp),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideStore({ cookie: cookieReducer }),
    provideHttpClient(
      withInterceptors([authInterceptor])
    )
  ]
};
