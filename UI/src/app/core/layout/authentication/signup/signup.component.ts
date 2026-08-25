import { Component, ViewChild, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms'
import { ActivatedRoute, Router } from '@angular/router';
import { SharedButtonComponent } from '../../../../shared/components/shared-button/shared-button.component';
import { SharedInputComponent } from '../../../../shared/components/shared-input/shared-input.component';
import { passwordValidator } from '../../../../shared/validators/password-validator';
import { Constants } from '../../../../shared/components/constants/constants';
import { MainModulesRoutingModule } from "../../../../features/main-modules/main-modules-routing.module";
import { UserSignInRequest } from '../../../../shared/interfaces/authentication.interface';
import { AuthenticationService } from '../../../services/authentication.service';
import { SharedToastNotificationComponent } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.component';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Subscription } from 'rxjs';
import { CartService } from '../../../services/cart.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule, SharedButtonComponent, SharedInputComponent, MainModulesRoutingModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  private router: Router = inject(Router);
  private route: ActivatedRoute = inject(ActivatedRoute);
  private authService: AuthenticationService = inject(AuthenticationService);
  private cartService: CartService = inject(CartService);
  private constants: Constants = inject(Constants);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private paramSubscrioption!: Subscription;

  readonly passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  signInForm: FormGroup = new FormGroup({
    firstName: new FormControl('', [Validators.required, Validators.minLength(2)]),
    lastName: new FormControl('', [Validators.required, Validators.minLength(2)]),
    emailAddress: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(8), Validators.pattern(this.passwordRegex)]),
    confirmPassword: new FormControl('', [Validators.required]),
    policyAccepted: new FormControl(false, [Validators.requiredTrue])
  }, {
    validators: [passwordValidator]
  });
  formSubmitted: boolean = false;
  formHasErrors: boolean = false;
  errorMessage: string = '';

  toastNotificationMessage: string = '';
  toastNotificationType: string = '';
  signinInProgress: boolean = false;

  returnUrl: string = '/home';

  ngOnInit(): void {
    this.paramSubscrioption = this.route.queryParams.subscribe(params => {
      this.returnUrl = params['returnUrl'] || '/home';
    });
  }

  checkFormErrors(): void {
    if (this.signInForm.invalid) {
      this.formHasErrors = true;
    } else {
      this.formHasErrors = false;
    }
  }

  setFormErrorMessage(): void {
    this.errorMessage = '';
    const firstNameControl: FormControl = this.signInForm.get('firstName') as FormControl;
    const lastNameControl: FormControl = this.signInForm.get('lastName') as FormControl;
    const emailAddressControl: FormControl = this.signInForm.get('emailAddress') as FormControl;
    const passwordControl: FormControl = this.signInForm.get('password') as FormControl;
    const confirmPasswordControl: FormControl = this.signInForm.get('confirmPassword') as FormControl;
    const policyAcceptedControl: FormControl = this.signInForm.get('policyAccepted') as FormControl;

    if (this.formHasErrors) {
      this.errorMessage = this.constants.GENERIC_ERROR_MESSAGE;
      if ((firstNameControl?.dirty || firstNameControl?.touched ||
        lastNameControl?.dirty || lastNameControl?.touched ||
        emailAddressControl?.dirty || emailAddressControl?.touched ||
        passwordControl?.dirty || passwordControl?.touched ||
        confirmPasswordControl?.dirty || confirmPasswordControl?.touched) &&
        (firstNameControl?.hasError('required') ||
          lastNameControl?.hasError('required') ||
          emailAddressControl?.hasError('required') ||
          passwordControl?.hasError('required') ||
          confirmPasswordControl?.hasError('required'))) {
        this.errorMessage = this.constants.signInLoginConstants.REQUIRED_ERROR_MESSAGE;
      } else if (policyAcceptedControl?.hasError('required')) {
        this.errorMessage = this.constants.signInLoginConstants.POLICY_NOT_ACCEPTED_ERROR_MESSAGE;
      } else if ((firstNameControl.dirty && firstNameControl.touched && firstNameControl?.hasError('minLength')) ||
        (lastNameControl.dirty && lastNameControl.touched && lastNameControl?.hasError('minLength'))) {
        this.errorMessage = this.constants.signInLoginConstants.MIN_LENGTH_VALIDATOR_ERROR_MESSAGE;
      } else if (emailAddressControl.dirty && emailAddressControl.touched && emailAddressControl?.hasError('email')) {
        this.errorMessage = this.constants.signInLoginConstants.EMAIL_FORMAT_ERROR_MESSAGE;
      } else if (passwordControl.dirty && passwordControl.touched && passwordControl?.hasError('pattern')) {
        this.errorMessage = this.constants.signInLoginConstants.PATTERN_VALIDATOR_ERROR_MESSAGE;
      } else if (confirmPasswordControl.dirty && confirmPasswordControl.touched && confirmPasswordControl?.hasError('passwordMismatch')) {

        this.errorMessage = this.constants.signInLoginConstants.PASSWORD_MISMATCH_VALIDATOR_ERROR_MESSAGE;
      }
    }
  }

  signInSubmission(): void {
    this.formSubmitted = true;
    this.signinInProgress = true;
    this.checkFormErrors();
    if (!this.formHasErrors) {
      const userSignInPayload: UserSignInRequest = {
        first_name: this.signInForm.get('firstName')?.value,
        last_name: this.signInForm.get('lastName')?.value,
        email_address: this.signInForm.get('emailAddress')?.value,
        password: this.signInForm.get('password')?.value
      }
      this.authService.userSignIn(userSignInPayload).subscribe((signInResponseMessage: string | null): void => {
        if (!signInResponseMessage) {
          this.toastNotificationMessage = 'Account created successfully.';
          this.toastNotificationType = this.constants.TOAST_NOTIFICATION_TYPES['SUCCESS'];
          this.sharedToastNotificationService.showNotification(this.toastNotificationMessage, this.toastNotificationType);
          this.authService.setWorkflowComplete(true);
          this.signinInProgress = false;
          this.router.navigate(['/home']);
        } else {
          this.signinInProgress = false;
          this.formHasErrors = true;
          this.errorMessage = signInResponseMessage;
        }
      });
    } else {
      this.signinInProgress = false;
      this.setFormErrorMessage();
    }
  }

  ngOnDestroy(): void {
    this.paramSubscrioption.unsubscribe();
  }
}
