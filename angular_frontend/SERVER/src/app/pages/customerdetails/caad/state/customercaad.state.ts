import { createFeatureSelector } from '@ngrx/store';
import * as customersCreationReducer from './customercaad.reducer';

export interface saveDraftState {
  saveDraftState: customersCreationReducer.DraftState;
}

export interface fetchedDraftsState {
  fetchedDraftState: customersCreationReducer.FetchedDraftState;
}

export const reducers = {
  draftReducer: customersCreationReducer.draftReducer,
  fetchedDraftReducer: customersCreationReducer.fetchedDraftReducer
  };

