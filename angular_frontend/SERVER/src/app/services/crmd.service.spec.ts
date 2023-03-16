import { TestBed } from '@angular/core/testing';

import { CrmdService } from './crmd.service';

describe('CrmdService', () => {
  let service: CrmdService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CrmdService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
