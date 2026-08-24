import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverallUserDetailsComponent } from './overall-user-details.component';

describe('OverallUserDetailsComponent', () => {
  let component: OverallUserDetailsComponent;
  let fixture: ComponentFixture<OverallUserDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverallUserDetailsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OverallUserDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
