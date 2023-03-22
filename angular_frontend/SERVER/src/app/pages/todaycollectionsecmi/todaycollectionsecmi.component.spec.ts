import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodaycollectionsecmiComponent } from './todaycollectionsecmi.component';

describe('TodaycollectionsecmiComponent', () => {
  let component: TodaycollectionsecmiComponent;
  let fixture: ComponentFixture<TodaycollectionsecmiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TodaycollectionsecmiComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodaycollectionsecmiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
