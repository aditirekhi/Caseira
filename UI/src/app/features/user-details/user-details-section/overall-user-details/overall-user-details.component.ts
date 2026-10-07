import { Component, inject } from '@angular/core';
import { CookieService } from '../../../../core/services/cookie.service';
import { AuthenticationResponse } from '../../../../shared/interfaces/authentication.interface';
import { UserService } from '../../../../core/services/user.service';

@Component({
  selector: 'app-overall-user-details',
  imports: [],
  templateUrl: './overall-user-details.component.html',
  styleUrl: './overall-user-details.component.css',
})
export class OverallUserDetailsComponent {
  private userService: UserService = inject(UserService);

  fetchUserName() {
  }
}
