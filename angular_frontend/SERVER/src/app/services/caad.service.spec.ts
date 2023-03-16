import { TestBed } from '@angular/core/testing';

import { CaadService } from './caad.service';

describe('CaadService', () => {
  let service: CaadService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CaadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
