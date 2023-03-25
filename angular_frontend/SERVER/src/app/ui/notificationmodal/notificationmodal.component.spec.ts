import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotificationmodalComponent } from './notificationmodal.component';

describe('NotificationmodalComponent', () => {
  let component: NotificationmodalComponent;
  let fixture: ComponentFixture<NotificationmodalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NotificationmodalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NotificationmodalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
