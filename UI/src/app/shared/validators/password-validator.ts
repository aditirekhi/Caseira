import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";

export const passwordValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (!password || !password.value || !confirmPassword || !confirmPassword.value) {
        return null;
    } else if (password.value !== confirmPassword.value) {
        confirmPassword.setErrors({ passwordMismatch: true })
        return { passwordMismatch: true };
    }
    return null;
}
