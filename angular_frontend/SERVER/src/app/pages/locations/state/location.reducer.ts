import { Locations } from '../models/location';
import { All, LocationActionTypes } from './location.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY

export interface State {
  isFetched:boolean;
  locations: Locations | null;
  errorMessage: string | null;
}

export const initialState: State = {
    isFetched:false,
    locations:null,
    errorMessage:null,
};

  export function reducer(state = initialState, action: All): State {
    switch (action.type) {
      case LocationActionTypes.FETCH_LOCATIONS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          locations: action.payload,
          errorMessage: null
        };
        return storeState;
      }
      case LocationActionTypes.FETCH_LOCATIONS_FAILURE: {
        return {
          ...state,
          errorMessage: 'An error occured while processing your request'
        };
      }
     
      default: {
        return state;
      }
    }
  } 