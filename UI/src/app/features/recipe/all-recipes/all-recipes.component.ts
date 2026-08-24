import { Component } from '@angular/core';
import { NavbarComponent } from "../../../core/layout/navbar/navbar.component";
import { FooterComponent } from "../../../core/layout/footer/footer.component";
import { SharedButtonComponent } from "../../../shared/components/shared-button/shared-button.component";

@Component({
  selector: 'app-all-recipes',
  imports: [NavbarComponent, FooterComponent, SharedButtonComponent],
  templateUrl: './all-recipes.component.html',
  styleUrl: './all-recipes.component.css',
})
export class AllRecipesComponent {

}
