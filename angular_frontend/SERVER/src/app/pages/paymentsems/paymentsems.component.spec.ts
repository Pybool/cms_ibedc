import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaymentsemsComponent } from './paymentsems.component';

describe('PaymentsemsComponent', () => {
  let component: PaymentsemsComponent;
  let fixture: ComponentFixture<PaymentsemsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PaymentsemsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaymentsemsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
