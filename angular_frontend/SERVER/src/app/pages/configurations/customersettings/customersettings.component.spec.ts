import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomersettingsComponent } from './customersettings.component';

describe('CustomersettingsComponent', () => {
  let component: CustomersettingsComponent;
  let fixture: ComponentFixture<CustomersettingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CustomersettingsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomersettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
