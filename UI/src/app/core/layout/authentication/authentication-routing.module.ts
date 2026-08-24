import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./login/login.component')
      .then(
        m => LoginComponent
      )
  },
  {
    path: 'signup',
    loadComponent: () => import('./signup/signup.component')
      .then(
        m => m.SignupComponent
      )
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./forgotten-password/forgotten-password.component')
      .then(
        m => m.ForgottenPasswordComponent
      )
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthenticationRoutingModule { }
