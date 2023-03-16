
import { All, CustomerCreationActionTypes } from './customercaad.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY


export interface DraftState {
  isSaved:boolean;
  draft_name: any | null;
  data:any | null;
  errorMessage: string | null;
}

export interface FetchedDraftState {
  isFetched:boolean;
  drafts: any | null;
  errorMessage: string | null;
}

export interface LoadDraftState {
  isLoaded:boolean;
  draft: any | null;
  errorMessage: string | null;
}

export const initialLastDraftState: DraftState = {
  isSaved:false,
    draft_name:null,
    data:null,
    errorMessage:null,
};

export const initialFectchedDraftState: FetchedDraftState = {
  isFetched:false,
    drafts:null,
    errorMessage:null,
};

export const initialLoadDraftDraftState: LoadDraftState ={
  isLoaded:false,
    draft:null,
    errorMessage:null,
}


  export function draftReducer(state = initialLastDraftState, action: All): DraftState {
    switch (action.type) {
      case CustomerCreationActionTypes.SAVE_DRAFT_SUCCESS: {
        let storeState = {
          ...state,
          isSaved: true,
          draft_name: action.payload.data.type,
          data: action.payload,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerCreationActionTypes.SAVE_DRAFT_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not save draft'
        };
      }
      
      default: {
        return state;
      }
    }
  } 


  export function fetchedDraftReducer(state = initialFectchedDraftState, action: All): FetchedDraftState {
    switch (action.type) {
      case CustomerCreationActionTypes.FETCH_DRAFTS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          drafts: action.payload.data,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerCreationActionTypes.FETCH_DRAFTS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch drafts'
        };
      }
      
      default: {
        return state;
      }
    }
  } 

  export function loadDraftReducer(state = initialLoadDraftDraftState, action: All): LoadDraftState {
    switch (action.type) {
      case CustomerCreationActionTypes.LOAD_DRAFT_SUCCESS: {
        let storeState = {
          ...state,
          isLoaded: true,
          draft: action.payload.data,
          errorMessage: null
        };
        return storeState;
      }
      case CustomerCreationActionTypes.LOAD_DRAFT_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch drafts'
        };
      }
      
      default: {
        return state;
      }
    }
  } 

  