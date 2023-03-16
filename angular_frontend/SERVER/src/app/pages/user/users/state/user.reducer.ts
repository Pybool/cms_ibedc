
import { All, UserActionTypes } from './user.actions';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
import { CreateUser } from '../../createuser/models/user';
const secretKey = environment.AES_SECRET_KEY

export interface State {
  isLoaded:boolean;
  user: CreateUser | null;
  errorMessage: string | null;
}

export interface UsersListState {
  isFetched:boolean;
  users: any | null;
  errorMessage: string | null;
}

export const initialState: State = {
    isLoaded:false,
    user:null,
    errorMessage:null,
};

export const initialUserListState: UsersListState = {
  isFetched:false,
  users:null,
  errorMessage:null,
};

  export function reducer(state = initialUserListState, action: All): UsersListState {
    switch (action.type) {
      case UserActionTypes.FETCH_USERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          users: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case UserActionTypes.FETCH_USERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch users'
        };
      }
      
      default: {
        return state;
      }
    }
  } 


  export function loadReducer(state = initialState, action: All): State {
    switch (action.type) {
      case UserActionTypes.FETCH_USERS_SUCCESS: {
        let storeState = {
          ...state,
          isFetched: true,
          users: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case UserActionTypes.FETCH_USERS_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not fetch users'
        };
      }
      case UserActionTypes.LOAD_USER_SUCCESS: {
        let storeState = {
          ...state,
          isLoaded: true,
          user: action.payload,
          errorMessage: null
        };
        // const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(storeState), secretKey).toString();
        // localStorage.setItem('appState', encryptedState);
        return storeState;
      }
      case UserActionTypes.LOAD_USER_FAILURE: {
        return {
          ...state,
          errorMessage: 'Could not load user.'
        };
      }
      
      default: {
        return state;
      }
    }
  } 