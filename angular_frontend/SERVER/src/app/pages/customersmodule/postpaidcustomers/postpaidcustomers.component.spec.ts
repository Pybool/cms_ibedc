import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostpaidcustomersComponent } from './postpaidcustomers.component';

describe('PostpaidcustomersComponent', () => {
  let component: PostpaidcustomersComponent;
  let fixture: ComponentFixture<PostpaidcustomersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PostpaidcustomersComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostpaidcustomersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
