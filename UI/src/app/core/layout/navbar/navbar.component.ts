import { Component, ChangeDetectionStrategy, HostListener } from '@angular/core';
import { RouterLinkActive } from '@angular/router';
import { SharedButtonComponent } from '../../../shared/components/shared-button/shared-button.component';
import { SharedInputComponent } from "../../../shared/components/shared-input/shared-input.component";
import { MainModulesRoutingModule } from "../../../features/main-modules/main-modules-routing.module";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLinkActive, SharedButtonComponent, SharedInputComponent, MainModulesRoutingModule],
  templateUrl: './navbar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  public screenWidth: number = 0;
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

  ngOnInit(): void {
    this.screenWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    this.screenWidth = window.innerWidth;
    if (this.screenWidth > 900) {
      this.showNavMenu = true;
    }
  }
}
