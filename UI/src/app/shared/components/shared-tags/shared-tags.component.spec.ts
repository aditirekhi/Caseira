import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SharedTagsComponent } from './shared-tags.component';

describe('SharedTagsComponent', () => {
  let component: SharedTagsComponent;
  let fixture: ComponentFixture<SharedTagsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedTagsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SharedTagsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
