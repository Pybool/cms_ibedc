import { createFeatureSelector } from '@ngrx/store';
import * as location from './location.reducer';


export interface locationsState {
  newUserState: location.State;
}

export const reducers = {
    locations: location.reducer
  };

