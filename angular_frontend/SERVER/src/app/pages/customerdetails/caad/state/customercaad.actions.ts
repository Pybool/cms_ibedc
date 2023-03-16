import { Action } from '@ngrx/store';


export enum CustomerCaadActionTypes {
  CREATE_CAAD = '[Caad] Create',
  CREATE_CAAD_SUCCESS = '[Caad] Create Successful',
  CREATE_CAAD_FAILURE = '[Caad] Create Failure',
  
  APPROVE_CAAD = '[Caad] Approval',
  APPROVE_CAAD_SUCCESS = '[Caad] Approval Successful',
  APPROVE_CAAD_FAILURE = '[Caad] Approval Failure',

  REVERT_CAAD = '[Caad] Revert',
  REVERT_CAAD_FAILURE = '[Caad] Revert Failure',
  REVERT_CAAD_SUCCESS = '[Caad] Revert Successful',

  UPDATE_CAAD = '[Caad] Update',
  UPDATE_CAAD_SUCCESS = '[Caad] Update Successful',
  UPDATE_CAAD_FAILURE = '[Caad] Update Failure',
  
}

export class CreateCaad implements Action {
  readonly type = CustomerCaadActionTypes.CREATE_CAAD;
  constructor(public payload: any) {}
}

export class CreateCaadSuccess implements Action {
  readonly type = CustomerCaadActionTypes.CREATE_CAAD_SUCCESS;
  constructor(public payload: any) {}
}

export class CreateCaadFailure implements Action {
  readonly type = CustomerCaadActionTypes.CREATE_CAAD_FAILURE;
  constructor(public payload: any) {}
}

export class ApproveCaad implements Action {
  readonly type = CustomerCaadActionTypes.APPROVE_CAAD;
  constructor(public payload: any) {}
}

export class ApproveCaadSuccess implements Action {
  readonly type = CustomerCaadActionTypes.APPROVE_CAAD_SUCCESS;
  constructor(public payload: any) {}
}

export class ApproveCaadFailure implements Action {
  readonly type = CustomerCaadActionTypes.APPROVE_CAAD_FAILURE;
  constructor(public payload: any) {}
}

export class RevertCaad implements Action {
  readonly type = CustomerCaadActionTypes.REVERT_CAAD;
  constructor() {}
}

export class RevertCaadSuccess implements Action {
  readonly type = CustomerCaadActionTypes.REVERT_CAAD_SUCCESS;
  constructor(public payload: any) {}
}

export class RevertCaadFailure implements Action {
  readonly type = CustomerCaadActionTypes.REVERT_CAAD_FAILURE;
  constructor(public payload: any) {}
}

export class UpdateCaad implements Action {
  readonly type = CustomerCaadActionTypes.UPDATE_CAAD;
  constructor(public payload: any) {}
}

export class UpdateCaadSuccess implements Action {
  readonly type = CustomerCaadActionTypes.UPDATE_CAAD_SUCCESS;
  constructor(public payload: any) {}
}

export class UpdateCaadFailure implements Action {
  readonly type = CustomerCaadActionTypes.UPDATE_CAAD_FAILURE;
  constructor(public payload: any) {}
}

export type All =
  | CreateCaad
  | CreateCaadSuccess
  | CreateCaadFailure
  | ApproveCaad
  | ApproveCaadSuccess
  | ApproveCaadFailure
  | RevertCaad
  | RevertCaadSuccess
  | RevertCaadFailure
  | UpdateCaad
  | UpdateCaadSuccess
  | UpdateCaadFailure
    