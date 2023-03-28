import * as customSel from './../ui/customselect/state/customselect.reducer';
import { createFeatureSelector } from '@ngrx/store';
import * as auth from '../authentication/state/auth.reducer';
import * as createUser from '../pages/user/state/createuser.reducer';
import * as userReducer from '../pages/user/users/state/user.reducer';
import * as custtomerReducer from '../pages/customersmodule/prepaidcustomers/state/customer.reducer';
import * as caadListReducer from '../pages/caadlist/state/caadlist.reducer';
import * as custtomerCreateReducer from '../pages/customercreation/state/customercreation.reducer';
import * as locationsReducer from '../pages/locations/state/location.reducer';

export interface AppState {
  authState: auth.State;
  createUserState: createUser.State;
  customSelectState: customSel.State;
  fetchedUsers:userReducer.UsersListState;
  loadedUser:userReducer.State,
  ecmiCustomers:custtomerReducer.ECMIState,
  emsCustomers:custtomerReducer.EMSState,
  deepFetchedEmsCustomers:custtomerReducer.DeepFetchEMSState,
  deepFetchedEcmiCustomers:custtomerReducer.DeepFetchECMIState,
  lastSavedDraft: custtomerCreateReducer.DraftState,
  fetchedDrafts:custtomerCreateReducer.FetchedDraftState,
  loadedDraft:custtomerCreateReducer.LoadDraftState,
  caadApprovalList: caadListReducer.State,
  locationsList: locationsReducer.State

}

export const reducers = {
    auth: auth.reducer,
    createUser:createUser.reducer,
    customSel:customSel.reducer,
    userpage: userReducer.reducer,
    loaduserForm:userReducer.loadReducer,
    ecmiCustomersList:custtomerReducer.ecmiReducer,
    emsCustomersList:custtomerReducer.emsReducer,
    // deepfetchEcmiCustomersList :custtomerReducer.deepFetchEcmiReducer,
    // deepfetchEmsCustomersList :custtomerReducer.deepFetchEmsReducer,
    lastSavedDraft:custtomerCreateReducer.draftReducer,
    fetchedDrafts:custtomerCreateReducer.fetchedDraftReducer,
    loadedDraft:custtomerCreateReducer.loadDraftReducer,
    caadApprovalList:caadListReducer.caadListReducer,
    locationsList: locationsReducer.reducer

  };

export const selectAuthState = createFeatureSelector<AppState>('auth');
export const selectcreateUserState = createFeatureSelector<AppState>('createUser');
export const selectcustomSelState = createFeatureSelector<AppState>('customSel');
export const selectuserpageState = createFeatureSelector<AppState>('userpage');