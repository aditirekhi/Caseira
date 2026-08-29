import { Component, ChangeDetectionStrategy, ChangeDetectorRef, inject } from '@angular/core';
import { CategoriesService } from '../../../core/services/categories.service';
import { FooterComponent } from "../../../core/layout/footer/footer.component";
import { SharedButtonComponent } from "../../../shared/components/shared-button/shared-button.component";
import { SharedTagsComponent } from "../../../shared/components/shared-tags/shared-tags.component";
import { FormsModule } from '@angular/forms';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../shared/components/constants/constants';
import { RecipesService } from '../../../core/services/recipes.service';
import { RecipeAllRequestQueryParams, RecipeCardInterface } from '../../../shared/interfaces/recipes.interface';
import { SharedRecipeCardComponent } from '../../../shared/components/shared-recipe-card/shared-recipe-card.component';
import { CommonModule } from '@angular/common';
import { RegionsService } from '../../../core/services/regions.service';
import { FetchAllRegionsResponse } from '../../../shared/interfaces/regions.interface';
import { AllCategoryDetailsInterface } from '../../../shared/interfaces/categories.interface';
import { SharedSkeletonComponent } from '../../../shared/components/shared-skeleton/shared-skeleton.component';

@Component({
  selector: 'app-all-recipes',
  imports: [CommonModule, FormsModule, FooterComponent, SharedButtonComponent, SharedTagsComponent, SharedRecipeCardComponent, SharedSkeletonComponent],
  templateUrl: './all-recipes.component.html',
  styleUrl: './all-recipes.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AllRecipesComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private recipeService: RecipesService = inject(RecipesService);
  private regionsService: RegionsService = inject(RegionsService);
  private categoriesService: CategoriesService = inject(CategoriesService);
  private constants: Constants = inject(Constants);

  showOnlyVegetarian: boolean = false;
  showOnlyNonVegetarian: boolean = false;

  recipeDetails: RecipeCardInterface[] = [];
  regionsDetails: FetchAllRegionsResponse[] = [];
  categoriesDetails: AllCategoryDetailsInterface[] = [];
  sortingOptions = this.constants.allRecipesConstants.SORTING_OPTIONS;
  selectedSortingOption: string = this.sortingOptions.MOST_POPULAR.label;

  isGridView: boolean = true;
  isRecipesLoading: boolean = true;
  isCategoryLoading: boolean = true;
  isRegionsLoading: boolean = true;
  showSortingOptions: boolean = false;

  ngOnInit() {
    this.fetchAllRecipes();
    this.fetchAllCategories();
    this.fetchAllRegions();
  }

  fetchAllCategories() {
    this.categoriesService.fetchAllCategories()
      .subscribe({
        next: (response: AllCategoryDetailsInterface[] | string) => {
          if (response && Array.isArray(response)) {
            this.categoriesDetails.push(...(response));
            this.changeDetection.markForCheck();
          } else {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          }
          this.isCategoryLoading = false;
          this.changeDetection.markForCheck();
        }, error: (error: string) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.isCategoryLoading = false;
          this.changeDetection.markForCheck();
        }
      });
  }

  getCategoryIcon(categoryName: string) {
    switch (categoryName) {
      case 'Appetizers':
        return 'fa-solid fa-utensils';
      case 'Beverages':
        return 'fa-solid fa-mug-hot';
      case 'Breakfast':
        return 'fa-solid fa-bread-slice';
      case 'Desserts':
        return 'fa-solid fa-cake-candles';
      case 'Dinner':
        return 'fa-solid fa-bowl-food';
      case 'Healthy Meals':
        return 'fa-solid fa-heart-pulse';
      case 'High Protein Meals':
        return 'fa-solid fa-drumstick-bite';
      case 'Lunch':
        return 'fa-solid fa-burger';
      case 'Quick Meals':
        return 'fa-solid fa-bolt';
      case 'Vegan':
        return 'fa-solid fa-seedling';
      default:
        return 'fa-solid fa-bowl-food';
    }
  }

  fetchAllRegions() {
    this.regionsService.getAllRegions().subscribe({
      next: (response: string | FetchAllRegionsResponse[]) => {
        if (response && Array.isArray(response)) {
          this.regionsDetails.push(...(response));
          this.changeDetection.markForCheck();
        } else {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
        this.isRegionsLoading = false;
        this.changeDetection.markForCheck();
      }, error: (error: string) => {
        this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        this.isRegionsLoading = false;
        this.changeDetection.markForCheck();
      }
    });
  }

  fetchAllRecipes() {
    const payload: RecipeAllRequestQueryParams = {
      order_by_field: this.constants.recipesConstants.RECIPE_FIELDS.NUMBER_OF_TOTAL_VISITS,
      order_by_direction: this.constants.SORTING_OPTIONS.ASCENDING,
      page_size: this.constants.recipesConstants.ALL_RECIPES_PAGE_SIZE
    };
    this.recipeService.fetchAllRecipes(payload).subscribe({
      next: (response: RecipeCardInterface[] | string) => {
        if (response && typeof response === 'string') {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        } else if (response && Array.isArray(response)) {
          this.recipeDetails.push(...(response));
        }
        this.isRecipesLoading = false;
        this.changeDetection.markForCheck();
      }, error: (error: string) => {
        this.isRecipesLoading = false;
        this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        this.changeDetection.markForCheck();
      }
    })
  }

  toggleVegetarianFilter() {
    this.showOnlyVegetarian = !this.showOnlyVegetarian;
  }

  toggleNonVegetarianFilter() {
    this.showOnlyNonVegetarian = !this.showOnlyNonVegetarian;
  }

  togglePageView() {
    this.isGridView = !this.isGridView;
  }

  toggleSortingOptions() {
    this.showSortingOptions = !this.showSortingOptions;
  }

  selectSortingOption(option: { label: string }) {
    this.selectedSortingOption = option.label;
    this.showSortingOptions = false;
  }

  closeSortingOptionsOnFocusOut(event: FocusEvent) {
    const wrapper = event.currentTarget as HTMLElement;
    const nextFocusedElement = event.relatedTarget as Node | null;

    if (!nextFocusedElement || !wrapper.contains(nextFocusedElement)) {
      this.showSortingOptions = false;
    }
  }
}
