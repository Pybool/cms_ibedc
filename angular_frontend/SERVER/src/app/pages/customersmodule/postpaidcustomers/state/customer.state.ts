import { createFeatureSelector } from '@ngrx/store';
import * as customersReducer from './customer.reducer';

export interface fetchedEmsCustomersState {
  fetchedUsersState: customersReducer.EMSState;
}

export const reducers = {
  emsCustomerReducer: customersReducer.emsReducer,
  // loaduserReducer:usersReducer.loadReducer
  };

