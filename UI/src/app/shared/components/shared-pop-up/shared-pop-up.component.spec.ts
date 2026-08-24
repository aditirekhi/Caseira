import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedPopUpComponent } from './shared-pop-up.component';

describe('SharedPopUpComponent', () => {
  let component: SharedPopUpComponent;
  let fixture: ComponentFixture<SharedPopUpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedPopUpComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedPopUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
