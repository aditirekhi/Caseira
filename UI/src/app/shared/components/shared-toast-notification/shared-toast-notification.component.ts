import { Component, input, InputSignal, inject } from '@angular/core';
import { Constants } from '../constants/constants';
import { SharedToastNotificationService } from './shared-toast-notification.service';
import { SharedButtonComponent } from "../shared-button/shared-button.component";

@Component({
  selector: 'shared-toast-notification',
  imports: [SharedButtonComponent],
  templateUrl: './shared-toast-notification.component.html',
  styleUrl: './shared-toast-notification.component.css',
})
export class SharedToastNotificationComponent {
  public sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  constants: Constants = new Constants();

  dismissToastNotification(notificationId: number): void {
    this.sharedToastNotificationService.dismiss(notificationId);
  }
}
