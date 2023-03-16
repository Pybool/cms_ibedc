import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComplaintsinformationComponent } from './complaintsinformation.component';

describe('ComplaintsinformationComponent', () => {
  let component: ComplaintsinformationComponent;
  let fixture: ComponentFixture<ComplaintsinformationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ComplaintsinformationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ComplaintsinformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
