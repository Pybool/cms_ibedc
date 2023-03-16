import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MeteringinformationComponent } from './meteringinformation.component';

describe('MeteringinformationComponent', () => {
  let component: MeteringinformationComponent;
  let fixture: ComponentFixture<MeteringinformationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MeteringinformationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MeteringinformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
