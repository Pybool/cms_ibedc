import { Action } from '@ngrx/store';


export enum UserActionTypes {
  FETCH_USERS = '[Users] Fetch',
  FETCH_USERS_SUCCESS = '[Users] Fetch Successful',
  FETCH_USERS_FAILURE = '[Users] Fetch Failure',
  LOAD_USER = '[User] Load',
  LOAD_USER_SUCCESS = '[User] Load Successful',
  LOAD_USER_FAILURE = '[User] Load Failure'
  
  
}

export class FetchUsers implements Action {
  readonly type = UserActionTypes.FETCH_USERS;
  constructor() {}
}

export class FetchUsersSuccess implements Action {
  readonly type = UserActionTypes.FETCH_USERS_SUCCESS;
  constructor(public payload: any) {}
}

export class FetchUsersFailure implements Action {
  readonly type = UserActionTypes.FETCH_USERS_FAILURE;
  constructor(public payload: any) {}
}
export class LoadUser implements Action {
    readonly type = UserActionTypes.LOAD_USER;
    constructor(public payload: any) {}
  }

export class LoadUserSuccess implements Action {
    readonly type = UserActionTypes.LOAD_USER_SUCCESS;
    constructor(public payload: any) {}
  }

export class LoadUserFailure implements Action {
    readonly type = UserActionTypes.LOAD_USER_FAILURE;
    constructor(public payload: any) {}
  }
  


export type All =
  | FetchUsers
  | FetchUsersSuccess
  | FetchUsersFailure
  | LoadUser
  | LoadUserSuccess
  | LoadUserFailure
  

    