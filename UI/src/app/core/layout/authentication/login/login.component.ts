import { Component, inject } from '@angular/core';
import { SharedInputComponent } from "../../../../shared/components/shared-input/shared-input.component";
import { SharedButtonComponent } from "../../../../shared/components/shared-button/shared-button.component";
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Constants } from '../../../../shared/components/constants/constants';
import { AuthenticationService } from '../../../services/authentication.service';
import { UserLogInRequest } from '../../../../shared/interfaces/authentication.interface';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Observable, Subscription, switchMap } from 'rxjs';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, SharedInputComponent, SharedButtonComponent, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  private router: Router = inject(Router);
  private route: ActivatedRoute = inject(ActivatedRoute);
  private constants: Constants = inject(Constants);
  private authService: AuthenticationService = inject(AuthenticationService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private paramSubscription!: Subscription;

  loginForm: FormGroup = new FormGroup({
    emailAddress: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', Validators.required)
  });
  hasErrors: boolean = false;
  errorMessage: string = '';

  toastNotificationMessage: string = '';
  toastNotificationType: string = '';
  returnUrl: string = '/home';

  loginInProgress: boolean = false;

  ngOnInit() {
    this.paramSubscription = this.route.queryParams.subscribe(params => {
      this.returnUrl = params['returnUrl'] || '/home';
    });
  }

  checkFormErrors(): void {
    if (this.loginForm.invalid) {
      this.hasErrors = true;
    } else {
      this.hasErrors = false;
    }
  }

  setErrorMessage(): void {
    this.errorMessage = '';
    const emailAddressControl: FormControl = this.loginForm.get('emailAddress') as FormControl;
    const passwordControl: FormControl = this.loginForm.get('password') as FormControl;

    this.checkFormErrors()
    if (this.hasErrors) {
      this.errorMessage = this.constants.GENERIC_ERROR_MESSAGE;
      if ((emailAddressControl.dirty || emailAddressControl.touched ||
        passwordControl.dirty || passwordControl.touched) &&
        emailAddressControl?.hasError('required') || passwordControl?.hasError('required')) {
        this.errorMessage = this.constants.signInLoginConstants.REQUIRED_ERROR_MESSAGE;
      } else if (emailAddressControl.dirty && emailAddressControl.touched && emailAddressControl?.hasError('email')) {
        this.errorMessage = this.constants.signInLoginConstants.EMAIL_FORMAT_ERROR_MESSAGE;
      }
    }
  }

  logInSubmission() {
    this.loginInProgress = true;
    this.checkFormErrors();
    if (!this.hasErrors) {
      const loginPayload: UserLogInRequest = {
        username: this.loginForm.get('emailAddress')?.value,
        password: this.loginForm.get('password')?.value
      }
      this.authService.userLogin(loginPayload)
        .subscribe((loginResponseMessage: string | null): void => {
          if (!loginResponseMessage) {
            this.toastNotificationMessage = this.constants.signInLoginConstants.LOGIN_SUCCESS_MESSAGE;
            this.toastNotificationType = this.constants.TOAST_NOTIFICATION_TYPES['SUCCESS'];
            this.sharedToastNotificationService.showNotification(this.toastNotificationMessage, this.toastNotificationType);
            this.authService.setWorkflowComplete(true);
            this.loginInProgress = false;
            this.router.navigate([this.returnUrl]);
            if (this.authService.hasPendingRequests()) {
              this.authService.processPendingRequests();
            }
          } else {
            this.loginInProgress = false;
            this.hasErrors = true;
            this.errorMessage = loginResponseMessage;
          }
        });
    } else {
      this.loginInProgress = false;
      this.setErrorMessage();
    }
  }

  ngOnDestroy() {
    this.paramSubscription.unsubscribe();
  }
}
