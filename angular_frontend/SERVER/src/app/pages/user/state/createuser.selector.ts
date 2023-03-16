import { createFeatureSelector, createSelector } from '@ngrx/store';
import { newUserState } from './createuser.state';
export const AUTH_STATE_NAME = 'auth';

const getAuthState = createFeatureSelector<newUserState>(AUTH_STATE_NAME);

export const isAuthenticated = createSelector(getAuthState, (state:any) => {
  console.log("State ====> ",state)
  return state.isAuthenticated ? true : false;
});

