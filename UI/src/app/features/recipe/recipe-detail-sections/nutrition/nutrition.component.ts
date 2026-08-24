import { Component, ChangeDetectionStrategy, ChangeDetectorRef, inject } from '@angular/core';
import { RecipesService } from '../../../../core/services/recipes.service';
import { RecipeDetailsInterface } from '../../../../shared/interfaces/recipes.interface';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../../shared/components/constants/constants';
import { JsonPipe, KeyValuePipe } from '@angular/common';

@Component({
  selector: 'app-nutrition',
  imports: [KeyValuePipe, JsonPipe],
  templateUrl: './nutrition.component.html',
  styleUrl: './nutrition.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NutritionComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
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
          if (response) {
            this.recipeDetails = response;
            this.changeDetection.markForCheck();
          }
        },
        error: (error: any) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  assignIconClass(nutritionName: any): string {
    if (!nutritionName || typeof nutritionName !== 'string') {
      return '';
    }

    const lowerCaseNutritionName = nutritionName.toLowerCase();

    switch (true) {
      case lowerCaseNutritionName.includes('calories'):
        return 'pi pi-bolt';
      case lowerCaseNutritionName.includes('protein'):
        return 'pi pi-wave-pulse';
      case lowerCaseNutritionName.includes('carbohydrates'):
        return 'pi pi-chart-bar';
      case lowerCaseNutritionName.includes('fat'):
        return 'pi pi-circle';
      case lowerCaseNutritionName.includes('fiber'):
        return 'pi pi-leaf';
      case lowerCaseNutritionName.includes('sugar'):
        return 'pi pi-box';
      case lowerCaseNutritionName.includes('cholesterol'):
        return 'pi pi-heart';
      case lowerCaseNutritionName.includes('sodium'):
        return 'pi pi-filter';
      case lowerCaseNutritionName.includes('calcium'):
        return 'pi pi-circle';
      case lowerCaseNutritionName.includes('iron'):
        return 'pi pi-bolt';
      default:
        return 'pi pi-info-circle';
    }
  }
}
