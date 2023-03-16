import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CaadlistComponent } from './caadlist.component';

describe('CaadlistComponent', () => {
  let component: CaadlistComponent;
  let fixture: ComponentFixture<CaadlistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CaadlistComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CaadlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
