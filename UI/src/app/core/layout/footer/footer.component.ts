import { Component, inject } from '@angular/core';
import { SharedButtonComponent } from "../../../shared/components/shared-button/shared-button.component";
import { Constants } from '../../../shared/components/constants/constants';

@Component({
  selector: 'app-footer',
  imports: [SharedButtonComponent],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css',
})
export class FooterComponent {
  constants: Constants = inject(Constants);

  showExploreMenu: boolean = false;
  showHelpMenu: boolean = false;
  showCompanyMenu: boolean = false;
  showLegalMenu: boolean = false;
  showWeAcceptsMenu: boolean = false;

  toggleExploreMenu() {
    this.showExploreMenu = !this.showExploreMenu;
  }

  toggleHelpMenu() {
    this.showHelpMenu = !this.showHelpMenu;
  }

  toggleCompanyMenu() {
    this.showCompanyMenu = !this.showCompanyMenu;
  }

  toggleLegalMenu() {
    this.showLegalMenu = !this.showLegalMenu;
  }

  toggleWeAcceptsMenu() {
    this.showWeAcceptsMenu = !this.showWeAcceptsMenu;
  }
}
