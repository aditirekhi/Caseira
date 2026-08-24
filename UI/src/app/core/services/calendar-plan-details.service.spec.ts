import { TestBed } from '@angular/core/testing';

import { CalendarPlanDetailsService } from './calendar-plan-details.service';

describe('CalendarPlanDetailsService', () => {
  let service: CalendarPlanDetailsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CalendarPlanDetailsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
