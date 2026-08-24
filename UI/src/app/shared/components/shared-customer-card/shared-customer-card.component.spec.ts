import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedCustomerCardComponent } from './shared-customer-card.component';

describe('SharedCustomerCardComponent', () => {
  let component: SharedCustomerCardComponent;
  let fixture: ComponentFixture<SharedCustomerCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedCustomerCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedCustomerCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
