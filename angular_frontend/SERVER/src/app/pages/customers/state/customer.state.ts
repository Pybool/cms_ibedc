import { createFeatureSelector } from '@ngrx/store';
import * as customersReducer from './customer.reducer';

export interface fetchedEcmiCustomersState {
  fetchedUsersState: customersReducer.ECMIState;
}

export interface fetchedEmsCustomersState {
  fetchedUsersState: customersReducer.EMSState;
}

export const reducers = {
  ecmiCustomerReducer: customersReducer.ecmiReducer,
  emsCustomerReducer: customersReducer.emsReducer,
  // loaduserReducer:usersReducer.loadReducer
  };

