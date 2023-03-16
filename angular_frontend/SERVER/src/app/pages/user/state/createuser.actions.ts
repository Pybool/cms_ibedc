import { Action } from '@ngrx/store';


export enum UserActionTypes {
  CREATE_NEW_USER = '[User] Create',
  CREATE_USER_SUCCESS = '[User] Create User Success',
  CREATE_USER_FAILURE = '[User] Create User Failure',
  UPDATE_EXISTING_USER = '[User] Update',
  UPDATE_USER_SUCCESS = '[User] Update User Success',
  UPDATE_USER_FAILURE = '[User] Update User Failure',
  
}
export class CreateNewUser implements Action {
    readonly type = UserActionTypes.CREATE_NEW_USER;
    constructor(public payload: any) {}
  }
  export class UpdateExistingUser implements Action {
    readonly type = UserActionTypes.UPDATE_EXISTING_USER;
    constructor(public payload: any) {}
  }
export class CreateUserSuccess implements Action {
    readonly type = UserActionTypes.CREATE_USER_SUCCESS;
    constructor(public payload: any) {}
  }
export class CreateUserFailure implements Action {
    readonly type = UserActionTypes.CREATE_USER_FAILURE;
    constructor(public payload: any) {}
  }
  export class UpdateUserSuccess implements Action {
    readonly type = UserActionTypes.UPDATE_USER_SUCCESS;
    constructor(public payload: any) {}
  }

  export class UpdateUserFailure implements Action {
    readonly type = UserActionTypes.UPDATE_USER_FAILURE;
    constructor(public payload: any) {}
  }


export type All =
  | CreateNewUser
  | CreateUserSuccess
  | CreateUserFailure
  | UpdateUserSuccess
  | UpdateUserFailure
  | UpdateExistingUser



    