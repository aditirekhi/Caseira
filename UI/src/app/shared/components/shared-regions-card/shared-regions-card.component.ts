import { Component, input, inject } from '@angular/core';
import { SharedButtonComponent } from "../shared-button/shared-button.component";
import { RouterModule } from '@angular/router';
import { Constants } from '../constants/constants';

@Component({
  selector: 'shared-regions-card',
  standalone: true,
  imports: [SharedButtonComponent, RouterModule],
  templateUrl: './shared-regions-card.component.html',
  styleUrl: './shared-regions-card.component.css',
})
export class SharedRegionsCardComponent {
  constants: Constants = inject(Constants);

  regionId = input<string>('');
  regionName = input<string>('');
  noOfRecipes = input<number>(0);
  imageUrl = input<string>('');
}
