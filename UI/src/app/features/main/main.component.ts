import { Component, ChangeDetectionStrategy } from '@angular/core';
import { MainModule } from '../main-modules/main-modules.module';
import { NavbarComponent } from '../../core/layout/navbar/navbar.component';
import { FooterComponent } from '../../core/layout/footer/footer.component';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [MainModule, FooterComponent],
  templateUrl: './main.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './main.component.css'
})
export class MainComponent {

}
