import { createFeatureSelector } from '@ngrx/store';
import * as newUser from './createuser.reducer';


export interface newUserState {
  newUserState: newUser.State;
}

export const reducers = {
    newUser: newUser.reducer
  };

