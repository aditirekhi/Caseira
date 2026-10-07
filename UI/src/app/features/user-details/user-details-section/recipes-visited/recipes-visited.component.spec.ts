import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipesVisitedComponent } from './recipes-visited.component';

describe('RecipesVisitedComponent', () => {
  let component: RecipesVisitedComponent;
  let fixture: ComponentFixture<RecipesVisitedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecipesVisitedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RecipesVisitedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
