import { createFeatureSelector, createSelector } from '@ngrx/store';
import { saveDraftState } from './customercaad.state';
export const SAVED_DRAFT_STATE_NAME = 'lastSavedDraft';
export const FETCHED_DRAFTS_STATE_NAME = 'fetchedDrafts';
export const LOADED_DRAFTS_STATE_NAME = 'loadedDraft';


const lastSavedDraftSate = createFeatureSelector<saveDraftState>(SAVED_DRAFT_STATE_NAME);

const fetchedDraftsState = createFeatureSelector<saveDraftState>(FETCHED_DRAFTS_STATE_NAME);

const loadedDraftsState = createFeatureSelector<saveDraftState>(LOADED_DRAFTS_STATE_NAME);



export const lastSavedDraft = createSelector(lastSavedDraftSate, (state:any) => {
  return state
});

export const fetchedDrafts = createSelector(fetchedDraftsState, (state:any) => {
  return state
});

export const loadedDraft = createSelector(loadedDraftsState, (state:any) => {
  return state
});
