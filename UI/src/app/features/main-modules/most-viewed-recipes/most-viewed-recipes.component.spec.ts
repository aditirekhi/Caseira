import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { of } from 'rxjs';

import { RecipesService } from '../../../core/services/recipes.service';
import { Constants } from '../../../shared/components/constants/constants';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { MostViewedRecipesComponent } from './most-viewed-recipes.component';

describe('MostViewedRecipesComponent', () => {
  let component: MostViewedRecipesComponent;
  let fixture: ComponentFixture<MostViewedRecipesComponent>;
  let recipesService: jasmine.SpyObj<RecipesService>;
  let toastService: jasmine.SpyObj<SharedToastNotificationService>;

  beforeEach(async () => {
    recipesService = jasmine.createSpyObj('RecipesService', ['fetchAllRecipes']);
    toastService = jasmine.createSpyObj('SharedToastNotificationService', ['showNotification']);

    await TestBed.configureTestingModule({
      declarations: [MostViewedRecipesComponent],
      schemas: [NO_ERRORS_SCHEMA],
      providers: [
        { provide: RecipesService, useValue: recipesService },
        { provide: SharedToastNotificationService, useValue: toastService },
        {
          provide: Constants,
          useValue: {
            recipesConstants: {
              RECIPE_FIELDS: { NUMBER_OF_TOTAL_VISITS: 'number_of_total_visits' },
              MOST_VIEWED_RECIPES_PAGE_SIZE: 10,
              UNABLE_TO_FETCH_RECIPES_ERROR_MESSAGE: 'Unable to fetch recipes.'
            },
            SORTING_OPTIONS: { DESCENDING: 'desc' },
            TOAST_NOTIFICATION_TYPES: { ERROR: 'error' },
            GENERIC_ERROR_MESSAGE: 'Something went wrong.'
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(MostViewedRecipesComponent);
    component = fixture.componentInstance;
    recipesService.fetchAllRecipes.and.returnValue(of([]));
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should run ngOnInit', () => {
    const spy = spyOn(component, 'fetchMostViewedRecipes');
    component.ngOnInit();
    expect(spy).toHaveBeenCalled();
  });

  it('should run fetchMostViewedRecipes', () => {
    component.fetchMostViewedRecipes();
    expect(recipesService.fetchAllRecipes).toHaveBeenCalled();
  });

  it('should populate mostViewedRecipes with an array of RecipeCardInterface', () => {
    component.fetchMostViewedRecipes();
    expect(Array.isArray(component.mostViewedRecipes)).toBe(true);
  });

  it('should handle error in fetchMostViewedRecipes', () => {
    const errorMessage = 'Error fetching recipes';
    recipesService.fetchAllRecipes.and.returnValue(of(errorMessage));
    component.fetchMostViewedRecipes();
    expect(toastService.showNotification).toHaveBeenCalledWith(
      errorMessage,
      component['constants'].TOAST_NOTIFICATION_TYPES['ERROR']
    );
  });
});
