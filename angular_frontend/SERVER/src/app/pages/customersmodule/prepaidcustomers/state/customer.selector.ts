import { createFeatureSelector, createSelector } from '@ngrx/store';
import { fetchedEcmiCustomersState, fetchedEmsCustomersState } from './customer.state';
export const ECMI_CUSTOMERS_STATE_NAME = 'ecmiCustomersList';
export const EMS_CUSTOMERS_STATE_NAME = 'emsCustomersList';

const fetchedEcmiCustomersState = createFeatureSelector<fetchedEcmiCustomersState>(ECMI_CUSTOMERS_STATE_NAME);
const fetchedEmsCustomersState = createFeatureSelector<fetchedEmsCustomersState>(EMS_CUSTOMERS_STATE_NAME);


export const ecmiCustomers = createSelector(fetchedEcmiCustomersState, (state:any) => {
  console.log("State ====> ",state)
  return state
});

export const emsCustomers = createSelector(fetchedEmsCustomersState, (state:any) => {
  console.log("State ====> ",state)
  return state
});

