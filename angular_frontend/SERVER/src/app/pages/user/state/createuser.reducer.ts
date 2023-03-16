import { CreateUser } from '../createuser/models/user';
import { All, UserActionTypes } from './createuser.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY

export interface State {
  isCreated:boolean;
  user: CreateUser | null;
  errorMessage: string | null;
}

export const initialState: State = {
    isCreated:false,
    user:null,
    errorMessage:null,
};

  export function reducer(state = initialState, action: All): State {
    switch (action.type) {
      case UserActionTypes.CREATE_USER_SUCCESS: {
        let storeState = {
          ...state,
          isCreated: true,
          user: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case UserActionTypes.CREATE_USER_FAILURE: {
        return {
          ...state,
          errorMessage: 'An error occured while processing your request'
        };
      }
      case UserActionTypes.UPDATE_USER_SUCCESS: {
        return {
          ...state,
          errorMessage: ''
        };
      }
      // case UserActionTypes.UPDATE_USER_FAILURE: {
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