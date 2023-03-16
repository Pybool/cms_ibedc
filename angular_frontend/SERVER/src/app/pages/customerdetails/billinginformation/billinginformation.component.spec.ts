import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BillinginformationComponent } from './billinginformation.component';

describe('BillinginformationComponent', () => {
  let component: BillinginformationComponent;
  let fixture: ComponentFixture<BillinginformationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BillinginformationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BillinginformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
