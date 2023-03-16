import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomermainComponent } from './customermain.component';

describe('CustomermainComponent', () => {
  let component: CustomermainComponent;
  let fixture: ComponentFixture<CustomermainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CustomermainComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CustomermainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
