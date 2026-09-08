import { Component, ChangeDetectionStrategy, inject, WritableSignal, signal, HostListener } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { SharedToastNotificationComponent } from './shared/components/shared-toast-notification/shared-toast-notification.component';
import { CookieService } from './core/services/cookie.service';
import { LoadingPageComponent } from "./core/layout/loading-page/loading-page.component";
import { CartService } from './core/services/cart.service';
import { RecipesService } from './core/services/recipes.service';
import { Constants } from './shared/components/constants/constants';
import { NavbarComponent } from "./core/layout/navbar/navbar.component";
import { filter } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SharedToastNotificationComponent, LoadingPageComponent, NavbarComponent],
  templateUrl: './app.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Caseira';
  private router: Router = inject(Router);
  private cookieService = inject(CookieService);
  private cartService = inject(CartService);
  constants: Constants = inject(Constants);

  showNavBar: boolean = true;

  private hiddenRoute = '/auth';

  ngOnInit(): void {
    this.constants.primaryLoadingPage.set(true);
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.showNavBar = !event.urlAfterRedirects.includes(this.hiddenRoute);
    });
    this.cartService.fetchCartDetailsByUserId().subscribe({
      next: () => {
        this.constants.primaryLoadingPage.set(false);
      },
      error: (error) => {
        console.error('Cart initialization failed:', error);
        this.constants.primaryLoadingPage.set(false);
      }
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.constants.globalScreenWidth.set(window.innerWidth);
  }

  ngOnDestroy(): void {
    this.cookieService.clearCookieState();
  }
}
