import { Action } from '@ngrx/store';


export enum CustomerCreationActionTypes {
  SAVE_DRAFT = '[Draft] Save',
  SAVE_DRAFT_SUCCESS = '[Draft] Save Successful',
  SAVE_DRAFT_FAILURE = '[Draft] Save Failure',
  
  CREATE_AWAITING_CUSTOMER = '[Awaiting Customer] Create',
  CREATE_AWAITING_CUSTOMER_SUCCESS = '[Awaiting Customer] Create Successful',
  CREATE_AWAITING_CUSTOMER_FAILURE = '[Awaiting Customer] Create Failure',

  UPDATE_AWAITING_CUSTOMER = '[Awaiting Customer] Update',
  UPDATE_AWAITING_CUSTOMER_FAILURE = '[Awaiting Customer] Update Failure',
  UPDATE_AWAITING_CUSTOMER_SUCCESS = '[Awaiting Customer] Update Successful',

  LOAD_DRAFT = '[Draft] Load',
  LOAD_DRAFT_SUCCESS = '[Draft] Load Successful',
  LOAD_DRAFT_FAILURE = '[Draft] Load Failure',

  FETCH_DRAFTS = '[Draft] Fetch',
  FETCH_DRAFTS_SUCCESS = '[Draft] Fetch Successful',
  FETCH_DRAFTS_FAILURE = '[Draft] Fetch Failure'
  
}

export class SaveDraft implements Action {
  readonly type = CustomerCreationActionTypes.SAVE_DRAFT;
  constructor(public payload: any) {}
}

export class SaveDraftSuccess implements Action {
  readonly type = CustomerCreationActionTypes.SAVE_DRAFT_SUCCESS;
  constructor(public payload: any) {}
}

export class SaveDraftFailure implements Action {
  readonly type = CustomerCreationActionTypes.SAVE_DRAFT_FAILURE;
  constructor(public payload: any) {}
}

export class CreateAwaitingCustomer implements Action {
  readonly type = CustomerCreationActionTypes.CREATE_AWAITING_CUSTOMER;
  constructor(public payload: any) {}
}

export class CreateAwaitingCustomerSuccess implements Action {
  readonly type = CustomerCreationActionTypes.CREATE_AWAITING_CUSTOMER_SUCCESS;
  constructor(public payload: any) {}
}

export class CreateAwaitingCustomerFailure implements Action {
  readonly type = CustomerCreationActionTypes.CREATE_AWAITING_CUSTOMER_FAILURE;
  constructor(public payload: any) {}
}

export class UpdateAwaitingCustomer implements Action {
  readonly type = CustomerCreationActionTypes.UPDATE_AWAITING_CUSTOMER;
  constructor() {}
}

export class UpdateAwaitingCustomerSuccess implements Action {
  readonly type = CustomerCreationActionTypes.UPDATE_AWAITING_CUSTOMER_SUCCESS;
  constructor(public payload: any) {}
}

export class UpdateAwaitingCustomerFailure implements Action {
  readonly type = CustomerCreationActionTypes.UPDATE_AWAITING_CUSTOMER_FAILURE;
  constructor(public payload: any) {}
}

export class LoadDraft implements Action {
  readonly type = CustomerCreationActionTypes.LOAD_DRAFT;
  constructor(public payload: any) {}
}

export class LoadDraftSuccess implements Action {
  readonly type = CustomerCreationActionTypes.LOAD_DRAFT_SUCCESS;
  constructor(public payload: any) {}
}

export class LoadDraftFailure implements Action {
  readonly type = CustomerCreationActionTypes.LOAD_DRAFT_FAILURE;
  constructor(public payload: any) {}
}

export class FetchDrafts implements Action {
  readonly type = CustomerCreationActionTypes.FETCH_DRAFTS;
  constructor() {}
}

export class FetchDraftsSuccess implements Action {
  readonly type = CustomerCreationActionTypes.FETCH_DRAFTS_SUCCESS;
  constructor(public payload: any) {}
}

export class FetchDraftsFailure implements Action {
  readonly type = CustomerCreationActionTypes.FETCH_DRAFTS_FAILURE;
  constructor(public payload: any) {}
}



export type All =
  | SaveDraft
  | SaveDraftSuccess
  | SaveDraftFailure
  | CreateAwaitingCustomer
  | CreateAwaitingCustomerSuccess
  | CreateAwaitingCustomerFailure
  | UpdateAwaitingCustomer
  | UpdateAwaitingCustomerSuccess
  | UpdateAwaitingCustomerFailure
  | LoadDraft
  | LoadDraftSuccess
  | LoadDraftFailure
  | FetchDrafts
  | FetchDraftsSuccess
  | FetchDraftsFailure

    