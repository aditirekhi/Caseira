import { Component } from '@angular/core';
import { NavbarComponent } from "../../../core/layout/navbar/navbar.component";
import { UserSidebarComponent } from '../user-sidebar/user-sidebar.component';


@Component({
  selector: 'app-user-main',
  imports: [NavbarComponent, UserSidebarComponent],
  templateUrl: './user-main.component.html',
  styleUrl: './user-main.component.css',
})
export class UserMainComponent {

}
