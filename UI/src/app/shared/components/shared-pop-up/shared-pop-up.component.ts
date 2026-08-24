import { Component, input, output } from '@angular/core';
import { SharedButtonComponent } from "../shared-button/shared-button.component";

@Component({
  selector: 'shared-pop-up',
  imports: [SharedButtonComponent],
  templateUrl: './shared-pop-up.component.html',
  styleUrl: './shared-pop-up.component.css',
})
export class SharedPopUpComponent {
  popUpHeader = input<string>('');
  addIcon = input<boolean>(false);
  iconClass = input<string>('');

  dismissPopUpEvent = output<void>();
  confirmPopUpEvent = output<void>();

  dismissPopUp() {
    this.dismissPopUpEvent.emit();
  }

  confirmPopUp() {
    this.confirmPopUpEvent.emit();
  }
}
