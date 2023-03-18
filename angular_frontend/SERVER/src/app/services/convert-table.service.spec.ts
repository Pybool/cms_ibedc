import { TestBed } from '@angular/core/testing';

import { ConvertTableService } from './convert-table.service';

describe('ConvertTableService', () => {
  let service: ConvertTableService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConvertTableService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
