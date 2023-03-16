import { createFeatureSelector, createSelector } from '@ngrx/store';
import { AuthState } from './auth.state';
export const AUTH_STATE_NAME = 'auth';

const getAuthState = createFeatureSelector<AuthState>(AUTH_STATE_NAME);

export const isAuthenticated = createSelector(getAuthState, (state:any) => {
  console.log("State ====> ",state)
  return state.isAuthenticated ? true : false;
});

export const UserState = createSelector(getAuthState, (state:any) => {
  console.log("State ====> ",state)
  if(state.isAuthenticated==true){
    return state.user ;
  }
  else{
    //redirect to login
  }
  
});

export const getToken = createSelector(getAuthState, (state:any) => {
  return state.user.token ? state.user.token : null;
});
