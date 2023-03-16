import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaymentsinformationComponent } from './paymentsinformation.component';

describe('PaymentsinformationComponent', () => {
  let component: PaymentsinformationComponent;
  let fixture: ComponentFixture<PaymentsinformationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PaymentsinformationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PaymentsinformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
