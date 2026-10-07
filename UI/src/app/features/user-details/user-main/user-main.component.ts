import { Component } from '@angular/core';
import { UserSidebarComponent } from '../user-sidebar/user-sidebar.component';
import { AuthenticationRoutingModule } from '../../../core/layout/authentication/authentication-routing.module';


@Component({
  selector: 'app-user-main',
  imports: [UserSidebarComponent, AuthenticationRoutingModule],
  templateUrl: './user-main.component.html',
  styleUrl: './user-main.component.css',
})
export class UserMainComponent {

}
