import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedToastNotificationComponent } from './shared-toast-notification.component';

describe('SharedToastNotificationComponent', () => {
  let component: SharedToastNotificationComponent;
  let fixture: ComponentFixture<SharedToastNotificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedToastNotificationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedToastNotificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
