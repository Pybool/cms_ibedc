import { Action } from '@ngrx/store';


export enum CustomerActionTypes {
  FETCH_ECMI_CUSTOMERS = '[Ecmi Customers] Fetch',
  FETCH_ECMI_CUSTOMERS_SUCCESS = '[Ecmi Customers] Fetch Successful',
  FETCH_ECMI_CUSTOMERS_FAILURE = '[Ecmi Customers] Fetch Failure',
  FETCH_EMS_CUSTOMERS = '[Ems Customers] Fetch',
  FETCH_EMS_CUSTOMERS_SUCCESS = '[Ems Customers] Fetch Successful',
  FETCH_EMS_CUSTOMERS_FAILURE = '[Ems Customers] Fetch Failure',

  DEEP_FETCH_ECMI_CUSTOMERS = '[Ecmi Deep Customers] Fetch',
  DEEP_FETCH_ECMI_CUSTOMERS_FAILURE = '[Ecmi Deep Customers] Fetch Failure',
  DEEP_FETCH_ECMI_CUSTOMERS_SUCCESS = '[Ecmi Deep Customers] Fetch Successful',

  DEEP_FETCH_EMS_CUSTOMERS = '[Ems Deep Customers] Fetch',
  DEEP_FETCH_EMS_CUSTOMERS_SUCCESS = '[Ems Deep Customers] Fetch Successful',
  DEEP_FETCH_EMS_CUSTOMERS_FAILURE =  '[Ems Deep Customers] Fetch Failure',

  LOAD_EMS_CUSTOMER = '[Ems Customer] Load',
  LOAD_EMS_CUSTOMER_SUCCESS = '[Ems Customer] Load Successful',
  LOAD_EMS_CUSTOMER_FAILURE = '[Ems Customer] Load Failure'
  
}

export class FetchEcmiCustomers implements Action {
  readonly type = CustomerActionTypes.FETCH_ECMI_CUSTOMERS;
  constructor() {}
}

export class FetchEcmiCustomersSuccess implements Action {
  readonly type = CustomerActionTypes.FETCH_ECMI_CUSTOMERS_SUCCESS;
  constructor(public payload: any) {}
}

export class FetchEcmiCustomersFailure implements Action {
  readonly type = CustomerActionTypes.FETCH_ECMI_CUSTOMERS_FAILURE;
  constructor(public payload: any) {}
}

export class DeepFetchEcmiCustomers implements Action {
  readonly type = CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS;
  constructor(public payload: any) {}
}

export class DeepFetchEcmiCustomersSuccess implements Action {
  readonly type = CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_SUCCESS;
  constructor(public payload: any) {}
}

export class DeepFetchEcmiCustomersFailure implements Action {
  readonly type = CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_FAILURE;
  constructor(public payload: any) {}
}

export class FetchEmsCustomers implements Action {
  readonly type = CustomerActionTypes.FETCH_EMS_CUSTOMERS;
  constructor() {}
}

export class FetchEmsCustomersSuccess implements Action {
  readonly type = CustomerActionTypes.FETCH_EMS_CUSTOMERS_SUCCESS;
  constructor(public payload: any) {}
}

export class FetchEmsCustomersFailure implements Action {
  readonly type = CustomerActionTypes.FETCH_EMS_CUSTOMERS_FAILURE;
  constructor(public payload: any) {}
}



export class LoadEmsCustomer implements Action {
    readonly type = CustomerActionTypes.LOAD_EMS_CUSTOMER;
    constructor(public payload: any) {}
  }

export class LoadEmsCustomersuccess implements Action {
    readonly type = CustomerActionTypes.LOAD_EMS_CUSTOMER_SUCCESS;
    constructor(public payload: any) {}
  }

export class LoadEmsCustomerFailure implements Action {
    readonly type = CustomerActionTypes.LOAD_EMS_CUSTOMER_FAILURE;
    constructor(public payload: any) {}
  }
  
export type All =
  | FetchEcmiCustomers
  | FetchEcmiCustomersSuccess
  | FetchEcmiCustomersFailure
  | DeepFetchEcmiCustomers
  | DeepFetchEcmiCustomersSuccess
  | DeepFetchEcmiCustomersFailure
  | FetchEmsCustomers
  | FetchEmsCustomersSuccess
  | FetchEmsCustomersFailure
  | LoadEmsCustomer
  | LoadEmsCustomersuccess
  | LoadEmsCustomerFailure
  

    