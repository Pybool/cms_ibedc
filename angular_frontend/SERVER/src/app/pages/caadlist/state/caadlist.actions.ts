import { Action } from '@ngrx/store';


export enum CaadListActionTypes {

  FETCH_CAAD_LIST = '[Caad] FetchList',
  FETCH_CAAD_LIST_SUCCESS = '[Caad] FetchList Successful',
  FETCH_CAAD_LIST_FAILURE = '[Caad] FetchList Failure',


}

export class FetchCaadList implements Action {
  readonly type = CaadListActionTypes.FETCH_CAAD_LIST;
  constructor() {}
}

export class FetchCaadListSuccess implements Action {
  readonly type = CaadListActionTypes.FETCH_CAAD_LIST_SUCCESS;
  constructor(public payload: any) {}
}

export class FetchCaadListFailure implements Action {
  readonly type = CaadListActionTypes.FETCH_CAAD_LIST_FAILURE;
  constructor(public payload: any) {}
}



export type All =
  | FetchCaadList
  | FetchCaadListSuccess
  | FetchCaadListFailure
  
    