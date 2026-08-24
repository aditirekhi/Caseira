import { Component, ChangeDetectionStrategy } from '@angular/core';
import { SharedButtonComponent } from '../../../shared/components/shared-button/shared-button.component';
import { SharedInputComponent } from "../../../shared/components/shared-input/shared-input.component";
import { MainModulesRoutingModule } from "../../../features/main-modules/main-modules-routing.module";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [SharedButtonComponent, SharedInputComponent, MainModulesRoutingModule],
  templateUrl: './navbar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

}
