import { createFeatureSelector, createSelector } from '@ngrx/store';
import { caadListState } from './caadlist.state';
export const FETCHED_CAAD_LIST = 'caadApprovalList';


const caadApprovalList = createFeatureSelector<caadListState>(FETCHED_CAAD_LIST);


export const caadApprovalData = createSelector(caadApprovalList, (state:any) => {
  return state
});

