import { Component, input } from '@angular/core';
import { SharedButtonComponent } from "../shared-button/shared-button.component";
import { RouterModule } from '@angular/router';

@Component({
  selector: 'shared-regions-card',
  standalone: true,
  imports: [SharedButtonComponent, RouterModule],
  templateUrl: './shared-regions-card.component.html',
  styleUrl: './shared-regions-card.component.css',
})
export class SharedRegionsCardComponent {
  regionId = input<string>('');
  regionName = input<string>('');
  noOfRecipes = input<number>(0);
  imageUrl = input<string>('');
}
