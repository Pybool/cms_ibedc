import { createFeatureSelector } from '@ngrx/store';
import * as usersReducer from './user.reducer';


export interface loadedUserState {
  loadedUserState: usersReducer.State;

}

export interface fetchedUsersState {
  fetchedUsersState: usersReducer.UsersListState;
}

export const reducers = {
  usersReducer: usersReducer.reducer,
  loaduserReducer:usersReducer.loadReducer
  };

