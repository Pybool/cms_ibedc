import { User } from '../models/user';
import { All, AuthActionTypes } from './auth.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
const secretKey = environment.AES_SECRET_KEY

export interface State {
  isAuthenticated: boolean;
  user: User | null;
  errorMessage: string | null;
}

export const initialState: State = {
    isAuthenticated: false,
    user: null,
    errorMessage: null
  };

  export function reducer(state = initialState, action: All): State {
    switch (action.type) {
      case AuthActionTypes.LOGIN_SUCCESS: {
        let storeState = {
          ...state,
          isAuthenticated: true,
          user: action.payload,
          errorMessage: null
        };
        const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case AuthActionTypes.LOGIN_FAILURE: {
        return {
          ...state,
          errorMessage: 'Incorrect email and/or password.'
        };
      }
      case AuthActionTypes.VERIFY_OTP_FAILURE: {
        return {
          ...state,
          errorMessage: 'Incorrect otp supplied.'
        };
      }
      case AuthActionTypes.SIGNUP_SUCCESS: {
        return {
          ...state,
          isAuthenticated: true,
          user: {
            token: action.payload.token,
            email: action.payload.email
          },
          errorMessage: null
        };
      }
      case AuthActionTypes.SIGNUP_FAILURE: {
        return {
          ...state,
          errorMessage: 'That email is already in use.'
        };
      }
      case AuthActionTypes.LOGIN_FAILURE: {
        return {
          ...state,
          errorMessage: 'Incorrect email and/or password.'
        };
      }
      case AuthActionTypes.AUTH_REHYDRATE_SUCCESS: {
        let storeState = {
          ...state,
          isAuthenticated: !isNaN(action.payload.id),
          user: action.payload,
          errorMessage: null
        };
        console.log("reducing ===> ", action.payload)
        const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case AuthActionTypes.LOGOUT: {
        return initialState;
      }
      default: {
        return state;
      }
    }
  } 