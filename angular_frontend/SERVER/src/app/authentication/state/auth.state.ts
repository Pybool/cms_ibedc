import { createFeatureSelector } from '@ngrx/store';
import * as auth from './auth.reducer';


export interface AuthState {
  authState: auth.State;
}

export const reducers = {
    auth: auth.reducer
  };

