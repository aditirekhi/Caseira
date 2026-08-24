import { ChangeDetectionStrategy, Component, ChangeDetectorRef, inject } from '@angular/core';
import { SharedButtonComponent } from '../../../../shared/components/shared-button/shared-button.component';
import { ActivatedRoute } from '@angular/router';
import { distinctUntilChanged, filter, map, Subject, switchMap, takeUntil, tap } from 'rxjs';
import { ReviewsService } from '../../../../core/services/reviews.service';
import { SharedToastNotificationService } from '../../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../../shared/components/constants/constants';
import { RecipeDetailReviewResponse, RecipeReviewHelpfulResponse, RecipeReviewRequest, RecipeReviewResponse, TimeUnit, RecipeReviewRatingInput } from '../../../../shared/interfaces/recipe-review.interface';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-reviews',
  imports: [FormsModule, SharedButtonComponent],
  templateUrl: './reviews.component.html',
  styleUrl: './reviews.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReviewsComponent {
  private changeDetector: ChangeDetectorRef = inject(ChangeDetectorRef);
  private router: ActivatedRoute = inject(ActivatedRoute);
  private reviewService: ReviewsService = inject(ReviewsService);
  private sharedToastNotificationService: SharedToastNotificationService = inject(SharedToastNotificationService);
  private constants: Constants = inject(Constants)
  private destroy$: Subject<void> = new Subject<void>();

  recipeId: string | null = null;
  reviews: RecipeDetailReviewResponse | null = null;
  currentReviewId: string | null = null;
  sendingHelpfulReviewRequest: boolean = false;
  showReviewInput: boolean = false;
  reviewInputValue: string = '';
  reviewRatings: RecipeReviewRatingInput[] = [{
    index: 1,
    filled: false
  }, {
    index: 2,
    filled: false
  }, {
    index: 3,
    filled: false
  }, {
    index: 4,
    filled: false
  }, {
    index: 5,
    filled: false
  }];

  ngOnInit(): void {
    this.getRecipeIdFromRoute();
  }

  getRecipeIdFromRoute(): void {
    this.router.paramMap
      .pipe(
        map(paramMap => paramMap.get('id')),
        filter((id: string | null): id is string => id !== null),
        distinctUntilChanged(),
        tap((id: string) => {
          this.recipeId = id;
          this.changeDetector.markForCheck();
        }),
        switchMap((id: string) => {
          this.fetchReviewsForRecipeId(id);
          return [];
        }),
        takeUntil(this.destroy$)
      ).subscribe();
  }

  fetchReviewsForRecipeId(recipeId: string | null): void {
    if (!recipeId) {
      this.sharedToastNotificationService.showNotification('Recipe ID is missing.', 'error');
      return;
    }
    this.reviewService.fetchReviewDetailsByRecipeId(recipeId)
      .subscribe({
        next: (response: RecipeDetailReviewResponse | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.reviews = response;
            this.changeDetector.markForCheck();
          }
        },
        error: (error: any) => {
          this.sharedToastNotificationService.showNotification('An error occurred while fetching reviews.', this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
        }
      });
  }

  getRelativeTime(createDateInput: string | Date | number): string {
    const created = new Date(createDateInput);

    if (isNaN(created.getTime())) {
      return 'Invalid date';
    }

    const now = new Date();
    const diffInMs = created.getTime() - now.getTime();
    const diffInSeconds = Math.floor(diffInMs / 1000);
    const absSeconds = Math.abs(diffInSeconds);

    // Define exact time thresholds in seconds
    const min = 60;
    const hour = min * 60;
    const day = hour * 24;
    const month = day * 30;
    const year = day * 365;

    // Configuration mapping for thresholds and matching units
    const thresholds: { limit: number; value: number; unit: TimeUnit }[] = [
      { limit: min, value: 1, unit: 'second' },
      { limit: hour, value: min, unit: 'minute' },
      { limit: day, value: hour, unit: 'hour' },
      { limit: month, value: day, unit: 'day' },
      { limit: year, value: month, unit: 'month' },
    ];

    // Initialize native formatter (auto-handles plurals and local languages)
    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

    // Handle immediate "just now" fallback
    if (absSeconds < 10) {
      return 'just now';
    }

    // Iterate over thresholds to find correct unit breakdown
    for (const { limit, value, unit } of thresholds) {
      if (absSeconds < limit) {
        return rtf.format(Math.floor(diffInSeconds / value), unit);
      }
    }

    // Fallback default calculation for years
    return rtf.format(Math.floor(diffInSeconds / year), 'year');
  }


  getRange(count: number): number[] {
    return Array.from({ length: count }, (_, i) => i + 1);
  }

  hasHalfStar(rating: number): boolean {
    return rating % 1 !== 0;
  }

  toggleHelpfulReview(review: RecipeReviewResponse): void {
    this.sendingHelpfulReviewRequest = true;
    this.currentReviewId = review.recipe_review_id;
    this.changeDetector.markForCheck();
    if (review.helpful_review_given_by_user) {
      this.reviewService.deleteHelpfulReview(review.recipe_review_id)
        .subscribe({
          next: (response: RecipeReviewHelpfulResponse | string) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.fetchReviewsForRecipeId(this.recipeId);
            }
            this.sendingHelpfulReviewRequest = false;
            this.currentReviewId = null;
            this.changeDetector.markForCheck();
          },
          error: (error: any) => {
            this.sharedToastNotificationService.showNotification('An error occurred while deleting the helpful review.', this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            this.sendingHelpfulReviewRequest = false;
            this.currentReviewId = null;
            this.changeDetector.markForCheck();
          }
        });
    } else {
      this.reviewService.createHelpfulReview(review.recipe_review_id)
        .subscribe({
          next: (response: RecipeReviewHelpfulResponse | string) => {
            if (typeof response === 'string') {
              this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            } else {
              this.fetchReviewsForRecipeId(this.recipeId);
            }
            this.sendingHelpfulReviewRequest = false;
            this.currentReviewId = null;
            this.changeDetector.markForCheck();
          },
          error: (error: any) => {
            this.sharedToastNotificationService.showNotification('An error occurred while creating the helpful review.', this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
            this.sendingHelpfulReviewRequest = false;
            this.currentReviewId = null;
            this.changeDetector.markForCheck();
          }
        });
    }
  }

  showReviewInputContainer(): void {
    this.showReviewInput = true;
  }

  addRating(index: number): void {
    this.reviewRatings.forEach(rating => {
      rating.filled = rating.index <= index;
    });
  }

  submitReview(): void {
    const payload: RecipeReviewRequest = {
      ratings: this.reviewRatings.filter(rating => rating.filled).length,
      comment: this.reviewInputValue,
      recipe_id: this.recipeId
    };
    this.reviewService.updateReview(payload)
      .subscribe({
        next: (response: RecipeReviewResponse | string) => {
          if (typeof response === 'string') {
            this.sharedToastNotificationService.showNotification(response, this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          } else {
            this.sharedToastNotificationService.showNotification('Review submitted successfully.', this.constants.TOAST_NOTIFICATION_TYPES['SUCCESS']);
            this.fetchReviewsForRecipeId(this.recipeId);
            this.resetReviewInput();
            this.showReviewInput = false;
          }
          this.changeDetector.markForCheck();
        },
        error: (error: any) => {
          this.sharedToastNotificationService.showNotification('An error occurred while submitting the review.', this.constants.TOAST_NOTIFICATION_TYPES['ERROR']);
          this.changeDetector.markForCheck();
        }
      });
  }

  resetReviewInput(): void {
    this.reviewInputValue = '';
  }
}
