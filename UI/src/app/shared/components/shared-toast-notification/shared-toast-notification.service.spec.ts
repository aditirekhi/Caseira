import { TestBed } from '@angular/core/testing';

import { SharedToastNotificationService } from './shared-toast-notification.service';

describe('SharedToastNotificationService', () => {
  let service: SharedToastNotificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SharedToastNotificationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
