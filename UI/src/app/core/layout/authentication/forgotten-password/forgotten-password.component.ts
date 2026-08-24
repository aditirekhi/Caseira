import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';
import { passwordValidator } from '../../../../shared/validators/password-validator';
import { SharedButtonComponent } from '../../../../shared/components/shared-button/shared-button.component';
import { SharedInputComponent } from '../../../../shared/components/shared-input/shared-input.component';
import { Constants } from '../../../../shared/components/constants/constants';
import { AuthenticationService } from '../../../services/authentication.service';
import { ChangePasswordRequest } from '../../../../shared/interfaces/authentication.interface';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-forgotten-password',
  imports: [ReactiveFormsModule, RouterModule, SharedInputComponent, SharedButtonComponent],
  templateUrl: './forgotten-password.component.html',
  styleUrl: './forgotten-password.component.css',
})
export class ForgottenPasswordComponent {
  private router: Router = inject(Router);
  private route: ActivatedRoute = inject(ActivatedRoute);
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  public constants: Constants = inject(Constants);
  private authService: AuthenticationService = inject(AuthenticationService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private paramSubscription!: Subscription;

  passwordRegexPattern: string = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$';

  forgottenPasswordForm = new FormGroup({
    emailAddress: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(8), Validators.pattern(this.passwordRegexPattern)]),
    confirmPassword: new FormControl('', [Validators.required]),
  }, {
    validators: [passwordValidator]
  });
  hasErrors: boolean = false;
  errorMessage: string = '';
  returnUrl: string = '/home';

  ngOnInit() {
    this.paramSubscription = this.route.queryParams.subscribe(params => {
      this.returnUrl = params['returnUrl'] || '/home';
    })
  }

  private setErrorState(message: string): void {
    this.hasErrors = true;
    this.errorMessage = message || this.constants.signInLoginConstants.PASSWORD_RESET_FAILURE_MESSAGE;
    this.changeDetection.detectChanges();
  }

  checkFormErrors(): void {
    this.hasErrors = this.forgottenPasswordForm.invalid;
  }

  setErrorMessage(): void {
    this.errorMessage = '';
    const emailAddressControl: FormControl = this.forgottenPasswordForm.get('emailAddress') as FormControl;
    const passwordControl: FormControl = this.forgottenPasswordForm.get('password') as FormControl;
    const confirmPasswordControl: FormControl = this.forgottenPasswordForm.get('confirmPassword') as FormControl;

    this.checkFormErrors();
    if (this.hasErrors) {
      this.errorMessage = this.constants.GENERIC_ERROR_MESSAGE;
      if ((emailAddressControl.dirty || emailAddressControl.touched ||
        passwordControl.dirty || passwordControl.touched ||
        confirmPasswordControl.dirty || confirmPasswordControl.touched) &&
        (emailAddressControl?.hasError('required') || passwordControl?.hasError('required') || confirmPasswordControl?.hasError('required'))) {
        this.errorMessage = this.constants.signInLoginConstants.REQUIRED_ERROR_MESSAGE;
      } else if (emailAddressControl.dirty && emailAddressControl.touched && emailAddressControl?.hasError('email')) {
        this.errorMessage = this.constants.signInLoginConstants.EMAIL_FORMAT_ERROR_MESSAGE;
      } else if (passwordControl.dirty && passwordControl.touched && passwordControl?.hasError('pattern')) {
        this.errorMessage = this.constants.signInLoginConstants.PATTERN_VALIDATOR_ERROR_MESSAGE;
      } else if (confirmPasswordControl.dirty && confirmPasswordControl.touched && confirmPasswordControl?.hasError('passwordMismatch')) {
        this.errorMessage = this.constants.signInLoginConstants.PASSWORD_MISMATCH_VALIDATOR_ERROR_MESSAGE;
      }
    }
  }

  forgottenPasswordSubmission() {
    this.hasErrors = false;
    this.errorMessage = '';
    this.checkFormErrors();
    if (!this.hasErrors) {
      const emailAddress: string | null | undefined = this.forgottenPasswordForm.get('emailAddress')?.value;
      const password: string | null | undefined = this.forgottenPasswordForm.get('password')?.value;
      if (emailAddress && password) {
        const payload: ChangePasswordRequest = {
          email_address: emailAddress,
          new_password: password
        }
        this.authService.userForgotPassword(payload)
          .subscribe({
            next: (forgotPasswordMessage) => {
              if (!forgotPasswordMessage) {
                this.sharedToastNotificationService.showNotification(this.constants.signInLoginConstants.PASSWORD_RESET_SUCCESS_MESSAGE, this.constants.TOAST_NOTIFICATION_TYPES['SUCCESS']);
                this.router.navigate(['/auth/login']);
              } else {
                this.setErrorState(forgotPasswordMessage);
              }
            },
            error: (error) => {
              this.setErrorState(error.error?.detail ?? this.constants.signInLoginConstants.PASSWORD_RESET_FAILURE_MESSAGE);
            }
          });
      } else {
        this.setErrorState(this.constants.signInLoginConstants.PASSWORD_RESET_FAILURE_MESSAGE);
      }
    } else {
      this.setErrorMessage();
    }
  }

  ngOnDestroy() {
    this.paramSubscription.unsubscribe();
  }
}
