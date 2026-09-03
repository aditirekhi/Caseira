import { Component, inject } from '@angular/core';
import { Constants } from '../../../shared/components/constants/constants';

@Component({
  selector: 'app-hero-page',
  standalone: false,
  templateUrl: './hero-page.component.html',
  styleUrl: './hero-page.component.css',
})
export class HeroPageComponent {
  constants: Constants = inject(Constants);
}
