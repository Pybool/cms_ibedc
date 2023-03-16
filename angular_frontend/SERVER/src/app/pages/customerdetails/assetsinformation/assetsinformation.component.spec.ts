import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetsinformationComponent } from './assetsinformation.component';

describe('AssetsinformationComponent', () => {
  let component: AssetsinformationComponent;
  let fixture: ComponentFixture<AssetsinformationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AssetsinformationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssetsinformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
