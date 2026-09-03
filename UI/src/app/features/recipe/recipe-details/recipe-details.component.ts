import { Component, inject, ChangeDetectionStrategy, ChangeDetectorRef, HostListener } from '@angular/core';
import { ActivatedRoute, RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { RecipesService } from '../../../core/services/recipes.service';
import { RecipeDetailsInterface, ToogleRecipeFavoriteBookmarkStatus } from '../../../shared/interfaces/recipes.interface';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../shared/components/constants/constants';
import { SharedTagsComponent } from "../../../shared/components/shared-tags/shared-tags.component";
import { SharedButtonComponent } from "../../../shared/components/shared-button/shared-button.component";
import { distinctUntilChanged, filter, map, Subject, switchMap, takeUntil, tap } from 'rxjs';
import { CalendarPlanDetailsService } from '../../../core/services/calendar-plan-details.service';
import { UserCalendarPlanDetailsCreateUpdate } from '../../../shared/interfaces/user-calendar-plan-details';
import { DatePipe, NgClass } from '@angular/common';
import { MenuTab } from '../../../shared/interfaces/generic.interface';

@Component({
  selector: 'app-recipe-details',
  imports: [DatePipe, SharedTagsComponent, SharedButtonComponent, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './recipe-details.component.html',
  styleUrl: './recipe-details.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RecipeDetailsComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private activeRouter: ActivatedRoute = inject(ActivatedRoute);
  private router: Router = inject(Router);
  private recipeService: RecipesService = inject(RecipesService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private calendarPlanDetailsService: CalendarPlanDetailsService = inject(CalendarPlanDetailsService);
  private destroy$: Subject<void> = new Subject<void>();
  constants: Constants = inject(Constants);

  recipeId: string | null = null;
  recipeDetails: RecipeDetailsInterface | null = null;

  showCalendarInput: boolean = false;
  creatingUpdatingPlanDate: boolean = false;
  selectedPlanDate: string | null = null;
  addingRemovingBookmark: boolean = false;
  menuTab: MenuTab[] = [
    { label: 'Overview', route: '/overview', icon: 'fa-solid fa-info' },
    { label: 'Ingredients', route: '/ingredients', icon: 'fa-solid fa-basket-shopping' },
    { label: 'Step by Step', route: '/directions', icon: 'fa-solid fa-list-check' },
    { label: 'Nutrition', route: '/nutrition', icon: 'fa-solid fa-chart-simple' },
    { label: 'Reviews', route: '/reviews', icon: 'fa-solid fa-star' }
  ];
  selectedTab: string = 'Overview';

  ngOnInit() {
    this.listenRecipeDetails();
    this.fetchRecipeDetails();
  }

  listenRecipeDetails(): void {
    this.recipeService.recipeDetails$()
      .pipe(
        filter((response: RecipeDetailsInterface | null) => response !== null),
        takeUntil(this.destroy$)
      )
      .subscribe((response: RecipeDetailsInterface) => {
        this.recipeDetails = response;
        if (this.recipeDetails?.plan_date == this.constants.NONE_STRING) {
          this.recipeDetails.plan_date = null;
        }
        this.changeDetection.markForCheck();
      });
  }

  fetchRecipeDetails(): void {
    this.activeRouter.paramMap
      .pipe(
        map(paramMap => paramMap.get('id')),
        filter((id: string | null): id is string => id !== null),
        distinctUntilChanged(),
        tap((id: string) => {
          this.recipeId = id;
          this.recipeDetails = null;
          this.changeDetection.markForCheck();
        }),
        switchMap((id: string) => this.recipeService.fetchRecipeDetails(id)),
        takeUntil(this.destroy$)
      )
      .subscribe((response: string) => {
        if (response) {
          this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  getRange(num: number): number[] {
    return Array.from({ length: num }, (_, i) => i + 1);
  }

  hasHalfStar(rating: number): boolean {
    return rating % 1 !== 0;
  }

  onCalendarFocusOut(event: FocusEvent): void {
    const calendar = event.currentTarget as HTMLElement;
    const nextFocusedElement = event.relatedTarget as Node | null;

    if (!nextFocusedElement || !calendar.contains(nextFocusedElement)) {
      this.showCalendarInput = false;
      this.selectedPlanDate = '';
      this.changeDetection.markForCheck();
    }
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.showCalendarInput) {
      return;
    }

    const target = event.target as Element | null;
    if (!target?.closest('.add-to-plan-container')) {
      this.showCalendarInput = false;
      this.selectedPlanDate = '';
      this.changeDetection.markForCheck();
    }
  }

  onSelectingPlanDate($event: Event) {
    this.selectedPlanDate = ($event.target as HTMLInputElement).value;
  }

  onPlanDateChange() {
    if (!this.selectedPlanDate) {
      this.showCalendarInput = false;
      return;
    }

    if (
      this.recipeDetails?.plan_date &&
      this.toDateInputValue(this.recipeDetails.plan_date) === this.selectedPlanDate
    ) {
      return;
    }

    this.creatingUpdatingPlanDate = true;
    this.showCalendarInput = false;
    this.changeDetection.markForCheck();
    const payload: UserCalendarPlanDetailsCreateUpdate = {
      recipe_id: this.recipeId ?? '',
      plan_date: new Date(this.selectedPlanDate ?? '')
    }
    if (this.recipeDetails?.plan_date == null) {
      this.calendarPlanDetailsService.createPlannedDate(payload)
        .subscribe({
          next: (response) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.recipeDetails!.plan_date = new Date(response.plan_date).toDateString();
            }
            this.creatingUpdatingPlanDate = false;
            this.changeDetection.markForCheck();
          },
          error: (error) => {
            this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            this.creatingUpdatingPlanDate = false;
            this.changeDetection.markForCheck();
          }
        });
    } else if (this.recipeDetails?.plan_date !== this.selectedPlanDate) {
      this.calendarPlanDetailsService.updatePlannedDate(payload)
        .subscribe({
          next: (response) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.recipeDetails!.plan_date = new Date(response.plan_date).toDateString();
            }
            this.creatingUpdatingPlanDate = false;
            this.changeDetection.markForCheck();
          },
          error: (error) => {
            this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            this.creatingUpdatingPlanDate = false;
            this.changeDetection.markForCheck();
          }
        });
    }
  }

  addRemoveBookmarkForTheRecipe() {
    if (!this.recipeDetails || !this.recipeId) {
      return;
    }
    this.addingRemovingBookmark = true;
    this.changeDetection.markForCheck();

    if (!this.recipeDetails.is_bookmarked) {
      this.recipeService.addToBookmarks(this.recipeId).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.recipeDetails!.is_bookmarked = response.bookmarked;
            this.addingRemovingBookmark = false;
            this.changeDetection.markForCheck();
          }
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.addingRemovingBookmark = false;
          this.changeDetection.markForCheck();
        }
      });
    } else {
      this.recipeService.removeFromBookmarks(this.recipeId).subscribe({
        next: (response: ToogleRecipeFavoriteBookmarkStatus | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.recipeDetails!.is_bookmarked = response.bookmarked;
            this.addingRemovingBookmark = false;
            this.changeDetection.markForCheck();
          }
        },
        error: (error) => {
          this.sharedToastNotificationService.showNotification(error, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.addingRemovingBookmark = false;
          this.changeDetection.markForCheck();
        }
      });
    }
  }

  private toDateInputValue(value: string | Date): string {
    const date = value instanceof Date ? value : new Date(value);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
    this.recipeService.setRecipeDetails(null);
  }
}
