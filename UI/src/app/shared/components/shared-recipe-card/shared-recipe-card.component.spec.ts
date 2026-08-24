import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedRecipeCardComponent } from './shared-recipe-card.component';

describe('SharedRecipeCardComponent', () => {
  let component: SharedRecipeCardComponent;
  let fixture: ComponentFixture<SharedRecipeCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedRecipeCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedRecipeCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
