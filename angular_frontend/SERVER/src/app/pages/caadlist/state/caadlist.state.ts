import { createFeatureSelector } from '@ngrx/store';
import * as caadListReducer from './caadlist.reducer';

export interface caadListState {
  caadListState: caadListReducer.State;
}

export const reducers = {
  caadListReducer: caadListReducer.caadListReducer,
  };

