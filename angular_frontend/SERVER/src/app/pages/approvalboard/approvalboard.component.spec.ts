import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApprovalboardComponent } from './approvalboard.component';

describe('ApprovalboardComponent', () => {
  let component: ApprovalboardComponent;
  let fixture: ComponentFixture<ApprovalboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ApprovalboardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ApprovalboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
