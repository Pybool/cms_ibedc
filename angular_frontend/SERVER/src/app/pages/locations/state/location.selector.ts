import { createFeatureSelector, createSelector } from '@ngrx/store';
import { locationsState } from './location.state';
export const LOCATIONS_STATE_NAME = 'locationsList';

const getLocationsState = createFeatureSelector<locationsState>(LOCATIONS_STATE_NAME);

export const getLocations = createSelector(getLocationsState, (state:any) => {
  return state
});

