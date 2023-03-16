import { Action } from '@ngrx/store';


export enum CustomSelectActionTypes {
  FETCH_BUSINESS_HUBS = '[Locations] Fetch Business Hubs',
  FETCH_BUSINESS_HUBS_SUCCESS = '[Locations] Fetch Business Hubs Success',
  FETCH_BUSINESS_HUBS_FAILURE = '[Locations] Fetch Business Hubs Failure',
  FETCH_SERVICE_CENTERS = '[Locations] Fetch Service Centers',
  FETCH_SERVICE_CENTERS_SUCCESS = '[Locations] Fetch Service Centers Success',
  FETCH_SERVICE_CENTERS_FAILURE = '[Locations] Fetch Service Centers Failure',
  
}
export class FetchBusinessHubs implements Action {
    readonly type = CustomSelectActionTypes.FETCH_BUSINESS_HUBS;
    constructor(public payload: any) {console.log("Fetching Buiness Hubs for ", payload)}
  }
  export class FetchServiceCenters implements Action {
    readonly type = CustomSelectActionTypes.FETCH_SERVICE_CENTERS;
    constructor(public payload: any) {}
  }
export class FetchBusinessHubsSuccess implements Action {
    readonly type = CustomSelectActionTypes.FETCH_BUSINESS_HUBS_SUCCESS;
    constructor(public payload: any) {}
  }
export class FetchBusinessHubsFailure implements Action {
    readonly type = CustomSelectActionTypes.FETCH_BUSINESS_HUBS_FAILURE;
    constructor(public payload: any) {}
  }
  export class FetchServiceCentersSuccess implements Action {
    readonly type = CustomSelectActionTypes.FETCH_SERVICE_CENTERS_SUCCESS;
    constructor(public payload: any) {}
  }

  export class FetchServiceCentersFailure implements Action {
    readonly type = CustomSelectActionTypes.FETCH_SERVICE_CENTERS_FAILURE;
    constructor(public payload: any) {}
  }


export type All =
  | FetchBusinessHubs
  | FetchServiceCenters
  | FetchBusinessHubsSuccess
  | FetchBusinessHubsFailure
  | FetchServiceCentersSuccess
  | FetchServiceCentersFailure



    