import { createFeatureSelector, createSelector } from '@ngrx/store';
import { loadedUserState,fetchedUsersState } from './user.state';
export const USERS_STATE_NAME = 'userpage';
// export const USER_FORM_STATE_NAME = 'loaduserform';

// const getUserState = createFeatureSelector<loadedUserState>(USER_FORM_STATE_NAME);
const fetchedUsersState = createFeatureSelector<loadedUserState>(USERS_STATE_NAME);

// export const loadUser = createSelector(getUserState, (state:any) => {
//   console.log("State ====> ",state)
//   return state//.isLoaded ? true : false;
// });


export const usersData = createSelector(fetchedUsersState, (state:any) => {
  console.log("State ====> ",state)
  return state//.fetched ? true : false;
});

