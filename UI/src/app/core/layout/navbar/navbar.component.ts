import { Component, ChangeDetectionStrategy, inject } from '@angular/core';
import { RouterLinkActive } from '@angular/router';
import { SharedButtonComponent } from '../../../shared/components/shared-button/shared-button.component';
import { MainModulesRoutingModule } from "../../../features/main-modules/main-modules-routing.module";
import { Constants } from '../../../shared/components/constants/constants';
import { MenuTab } from '../../../shared/interfaces/generic.interface';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLinkActive, SharedButtonComponent, MainModulesRoutingModule],
  templateUrl: './navbar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  constants: Constants = inject(Constants);

  navbarMenuItems: MenuTab[] = [
    { label: 'Recipes', route: '/recipe/all' },
    { label: 'Ingredients', route: '/ingredients' },
    {
      label: 'Meal Kits', route: '/meal-kits'
    },
    { label: 'Regions', route: '/regions/all' },
    { label: 'Offers', route: '/offers' }
  ]

  public showNavMenu: boolean = false;
  public showSearchBox: boolean = false;

  toggleNavMenu(): void {
    this.showNavMenu = !this.showNavMenu;
  }

  closeNavMenu(): void {
    this.showNavMenu = false;
  }

  toggleSearchBox(): void {
    this.showSearchBox = !this.showSearchBox;
  }
}
