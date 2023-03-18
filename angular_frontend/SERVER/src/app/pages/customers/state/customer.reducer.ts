
import { All, CustomerActionTypes } from './customer.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
import { ECMICustomer } from '../models/customer';
const secretKey = environment.AES_SECRET_KEY

ECMICustomer

export interface ECMIState {
  isFetched:boolean;
  customers: ECMICustomer | null;
  timestamp:any | null;
  total_customers:number | 0,
  errorMessage: string | null;
}

export interface EMSState {
  isFetched:boolean;
  customers: any | null;
  timestamp:any | null;
  total_customers:number | 0,
  errorMessage: string | null;
}

export interface DeepFetchECMIState {
  isFetched:boolean;
  customers: any | null;
  timestamp:any | null;
  total_customers:number | 0,
  search_parameters:any | [],
  errorMessage: string | null;
}

export interface DeepFetchEMSState {
  isFetched:boolean;
  customers: any | null;
  timestamp:any | null;
  total_customers:number | 0,
  search_parameters:any | [],
  errorMessage: string | null;
}

export const initialECMIListState: ECMIState = {
  isFetched:false,
    customers:null,
    timestamp:null,
    total_customers:0,
    errorMessage:null,
};

export const initialDeepFetchECMIListState: DeepFetchECMIState = {
  isFetched:false,
    customers:null,
    timestamp:null,
    total_customers:0,
    search_parameters:[],
    errorMessage:null,
};

export const initialEMSListState: EMSState = {
  isFetched:false,
  customers:null,
  timestamp:null,
  total_customers:0,
  errorMessage:null,
};

export const initialDeepFetchEMSListState: DeepFetchEMSState = {
  isFetched:false,
    customers:null,
    timestamp:null,
    total_customers:0,
    search_parameters:[],
    errorMessage:null,
};

  export function ecmiReducer(state = initialECMIListState, action: All): ECMIState {
    switch (action.type) {
      case CustomerActionTypes.FETCH_ECMI_CUSTOMERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          customers: action.payload.data,
          timestamp: action.payload.timestamp,
          total_customers:action.payload.total_customers,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerActionTypes.FETCH_ECMI_CUSTOMERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch Customer'
        };
      }
      
      default: {
        return state;
      }
    }
  } 

  export function deepFetchEcmiReducer(state = initialDeepFetchECMIListState, action: All): DeepFetchECMIState {
    switch (action.type) {
      case CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          customers: action.payload.data,
          timestamp: 190,
          total_customers:action.payload.total_customers,
          search_parameters:action.payload.parameters,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not search for the record'
        };
      }
      
      default: {
        return state;
      }
    }
  } 


  export function emsReducer(state = initialEMSListState, action: All): EMSState {
    switch (action.type) {
      case CustomerActionTypes.FETCH_EMS_CUSTOMERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          customers: action.payload.data,
          timestamp: new Date().getTime(),
          total_customers:action.payload.total_customers,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case CustomerActionTypes.FETCH_EMS_CUSTOMERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch users'
        };
      }

      default: {
        return state;
      }
    }
  } 


  export function deepFetchEmsReducer(state = initialDeepFetchEMSListState, action: All): DeepFetchEMSState {
    switch (action.type) {
      case CustomerActionTypes.DEEP_FETCH_EMS_CUSTOMERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          customers: action.payload.data,
          timestamp: new Date().getTime(),
          total_customers:action.payload.total_customers,
          search_parameters:action.payload.parameters,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerActionTypes.DEEP_FETCH_EMS_CUSTOMERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not search for the record'
        };
      }
      
      default: {
        return state;
      }
    }
  } 