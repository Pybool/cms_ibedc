import { Action } from '@ngrx/store';


export enum LocationActionTypes {
  FETCH_LOCATIONS = '[Locations] Fetch',
  FETCH_LOCATIONS_SUCCESS = '[Locations] Fetch Success',
  FETCH_LOCATIONS_FAILURE = '[Locations] Fetch Failure',
  CREATE_LOCATIONS = '[Locations] Create',
  CREATE_LOCATIONS_SUCCESS = '[Locations] Create Success',
  CREATE_LOCATIONS_FAILURE = '[Locations] Create Failure',

}
export class FetchLocations implements Action {
    readonly type = LocationActionTypes.FETCH_LOCATIONS;
    constructor() {}
  }

export class FetchLocationsSuccess implements Action {
    readonly type = LocationActionTypes.FETCH_LOCATIONS_SUCCESS;
    constructor(public payload: any) {}
  }
export class FetchLocationsFailure implements Action {
    readonly type = LocationActionTypes.FETCH_LOCATIONS_FAILURE;
    constructor(public payload: any) {}
  }

export class CreateLocations implements Action {
    readonly type = LocationActionTypes.CREATE_LOCATIONS;
    constructor(public payload: any) {}
  }

export class CreateLocationsSuccess implements Action {
    readonly type = LocationActionTypes.CREATE_LOCATIONS_SUCCESS;
    constructor(public payload: any) {}
  }
export class CreateLocationsFailure implements Action {
    readonly type = LocationActionTypes.CREATE_LOCATIONS_FAILURE;
    constructor(public payload: any) {}
  }


export type All =
  | FetchLocations
  | FetchLocationsSuccess
  | FetchLocationsFailure
  | CreateLocations
  | CreateLocationsSuccess
  | CreateLocationsFailure
 