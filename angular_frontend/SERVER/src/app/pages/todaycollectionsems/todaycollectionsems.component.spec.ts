import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodaycollectionsemsComponent } from './todaycollectionsems.component';

describe('TodaycollectionsemsComponent', () => {
  let component: TodaycollectionsemsComponent;
  let fixture: ComponentFixture<TodaycollectionsemsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TodaycollectionsemsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodaycollectionsemsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
