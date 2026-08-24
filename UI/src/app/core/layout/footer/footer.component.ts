import { Component } from '@angular/core';
import { SharedInputComponent } from "../../../shared/components/shared-input/shared-input.component";
import { SharedButtonComponent } from "../../../shared/components/shared-button/shared-button.component";

@Component({
  selector: 'app-footer',
  imports: [SharedInputComponent, SharedButtonComponent],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css',
})
export class FooterComponent {

}
