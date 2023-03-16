import { createFeatureSelector } from '@ngrx/store';
import * as customSelect from './customselect.reducer';


export interface customSelectState {
  customSelectState: customSelect.State;
}

export const reducers = {
    customSelect: customSelect.reducer
  };

