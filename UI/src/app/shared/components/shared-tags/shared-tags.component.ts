import { Component, input } from '@angular/core';
import { FirstLetterCapitalPipe } from '../../pipes/first-letter-capital.pipe';

@Component({
  selector: 'shared-tags',
  imports: [FirstLetterCapitalPipe],
  templateUrl: './shared-tags.component.html',
  styleUrl: './shared-tags.component.css',
})
export class SharedTagsComponent {
  tagName = input<string>('');
  tagClass = input<string>('');
  addIcon = input<boolean>(false);
  iconClass = input<string>('');
  leftIcon = input<boolean>(false);
}
