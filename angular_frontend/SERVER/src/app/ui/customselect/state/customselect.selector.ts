import { createFeatureSelector, createSelector } from '@ngrx/store';
import { customSelectState } from './customselect.state';
export const CUSTOM_SELECT_STATE_NAME = 'customSel';

const customSelectDataState = createFeatureSelector<customSelectState>(CUSTOM_SELECT_STATE_NAME);

export const getLocationsState = createSelector(customSelectDataState, (state:any) => {
  console.log("Locations Business hubs ====> ",state)
  return {state:state,type:'business_units'}
});

export const getServiceCenters = createSelector(customSelectDataState, (state:any) => {
  console.log("Locations service centers ====> ",state)
  return {state:state,type:'service_centers'}
});

