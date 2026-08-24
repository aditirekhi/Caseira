import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedRegionsCardComponent } from './shared-regions-card.component';

describe('SharedRegionsCardComponent', () => {
  let component: SharedRegionsCardComponent;
  let fixture: ComponentFixture<SharedRegionsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedRegionsCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedRegionsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
