import { All, CustomSelectActionTypes } from './customselect.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY

export interface State {
  isFetched:boolean;
  location: any | null;
  errorMessage: string | null;
}

export const initialState: State = {
    isFetched:false,
    location:null,
    errorMessage:null,
};

  export function reducer(state = initialState, action: All): State {
    switch (action.type) {
      case CustomSelectActionTypes.FETCH_BUSINESS_HUBS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          location: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case CustomSelectActionTypes.FETCH_BUSINESS_HUBS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch business hubs'
        };
      }
      case CustomSelectActionTypes.FETCH_SERVICE_CENTERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          location: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case CustomSelectActionTypes.FETCH_SERVICE_CENTERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch service centers'
        };
      }
      // case CustomSelectActionTypes.UPDATE_USER_FAILURE: {
      //   return {
      //     ...state,
      //     isAuthenticated: true,
      //     user: {
      //       name: action.payload.token,
      //       email: action.payload.email
      //     },
      //     errorMessage: null
      //   };
      // }
     
      default: {
        return state;
      }
    }
  } 