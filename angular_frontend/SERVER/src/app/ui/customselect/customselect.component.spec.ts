import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomselectComponent } from './customselect.component';

describe('CustomselectComponent', () => {
  let component: CustomselectComponent;
  let fixture: ComponentFixture<CustomselectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CustomselectComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomselectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
