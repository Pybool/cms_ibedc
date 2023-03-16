import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CaadComponent } from './caad.component';

describe('CaadComponent', () => {
  let component: CaadComponent;
  let fixture: ComponentFixture<CaadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CaadComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CaadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
