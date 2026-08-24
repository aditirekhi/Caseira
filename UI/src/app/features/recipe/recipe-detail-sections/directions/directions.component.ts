import { Component, ChangeDetectionStrategy, ChangeDetectorRef, inject } from '@angular/core';
import { RecipeDetailsInterface } from '../../../../shared/interfaces/recipes.interface';
import { RecipesService } from '../../../../core/services/recipes.service';
import { KeyValuePipe } from '@angular/common';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../../shared/components/constants/constants';

@Component({
  selector: 'app-directions',
  imports: [KeyValuePipe],
  templateUrl: './directions.component.html',
  styleUrl: './directions.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DirectionsComponent {
  private changeDetection = inject(ChangeDetectorRef);
  private constants: Constants = inject(Constants);
  private recipeService: RecipesService = inject(RecipesService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  recipeDetails: RecipeDetailsInterface | null = null;

  ngOnInit() {
    this.fetchRecipeDetails();
  }

  fetchRecipeDetails(): void {
    this.recipeService.recipeDetails$()
      .subscribe({
        next: (response: RecipeDetailsInterface | null) => {
          this.recipeDetails = response;
          this.changeDetection.markForCheck();
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }
}
