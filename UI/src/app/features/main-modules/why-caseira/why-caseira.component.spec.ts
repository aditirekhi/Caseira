import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhyCaseiraComponent } from './why-caseira.component';

describe('WhyCaseiraComponent', () => {
  let component: WhyCaseiraComponent;
  let fixture: ComponentFixture<WhyCaseiraComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WhyCaseiraComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WhyCaseiraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
