import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExploreByRegionsComponent } from './explore-by-regions.component';

describe('ExploreByRegionsComponent', () => {
  let component: ExploreByRegionsComponent;
  let fixture: ComponentFixture<ExploreByRegionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExploreByRegionsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExploreByRegionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
