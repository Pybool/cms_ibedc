
import { All, CaadListActionTypes } from './caadlist.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY


export interface State {
  isFetched:boolean;
  data: any | null;
  errorMessage: string | null;
}

export const initialCaadListState: State = {
  isFetched:false,
    data:null,
    errorMessage:null,
};


export function caadListReducer(state = initialCaadListState, action: All): State {
  switch (action.type) {
    case CaadListActionTypes.FETCH_CAAD_LIST_SUCCESS: {
      let storeState = {
        ...state,
        isFetched: true,
        data: action.payload,
        errorMessage: null
      };
      return storeState;
    }
    case CaadListActionTypes.FETCH_CAAD_LIST_FAILURE: {
      return {
        ...state,
        errorMessage: 'Could not fetch caad list '
      };
    }
    
    default: {
      return state;
    }
  }
} 


