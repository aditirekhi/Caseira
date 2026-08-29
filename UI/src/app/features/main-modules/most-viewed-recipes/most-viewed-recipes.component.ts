import { ChangeDetectorRef, ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RecipesService } from '../../../core/services/recipes.service';
import { RecipeCardInterface, RecipeAllRequestQueryParams } from '../../../shared/interfaces/recipes.interface';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../shared/components/constants/constants';

@Component({
  selector: 'app-most-viewed-recipes',
  standalone: false,
  templateUrl: './most-viewed-recipes.component.html',
  styleUrl: './most-viewed-recipes.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MostViewedRecipesComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private constants: Constants = inject(Constants);
  private recipesService: RecipesService = inject(RecipesService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);

  mostViewedRecipes: RecipeCardInterface[] = [];
  loadingMostViewedRecipes: boolean = true;

  ngOnInit() {
    this.fetchMostViewedRecipes();
  }

  fetchMostViewedRecipes() {
    this.constants.primaryLoadingPage.set(true);
    const queryParams: RecipeAllRequestQueryParams = {
      order_by_field: this.constants.recipesConstants.RECIPE_FIELDS.NUMBER_OF_TOTAL_VISITS,
      order_by_direction: this.constants.SORTING_OPTIONS.DESCENDING,
      page_size: this.constants.recipesConstants.MOST_VIEWED_RECIPES_PAGE_SIZE
    };
    this.recipesService.fetchAllRecipes(queryParams).subscribe({
      next: (recipes) => {
        this.mostViewedRecipes = Array.isArray(recipes) ? recipes : [];
        this.constants.primaryLoadingPage.set(false);
        this.loadingMostViewedRecipes = false;
        this.changeDetection.detectChanges();
      },
      error: (error) => {
        this.sharedToastNotificationService.showNotification(
          error || this.constants.recipesConstants.UNABLE_TO_FETCH_RECIPES_ERROR_MESSAGE,
          this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        this.constants.primaryLoadingPage.set(false);
        this.loadingMostViewedRecipes = false;
        this.changeDetection.detectChanges();
      }
    });
  }

  getMostViewedLength(): number[] {
    return Array(4);
  }
}
