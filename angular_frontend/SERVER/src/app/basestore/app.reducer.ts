import { ActionReducer } from '@ngrx/store';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';

const secretKey = environment.AES_SECRET_KEY;

export function getStoredState(): any {
    const savedState = localStorage.getItem('appState');
    if (savedState) {
      const bytes = CryptoJS.AES.decrypt(savedState, secretKey);
      const decryptedState = JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
      return decryptedState;
    }
    return {};
  }
  
export function localStorageReducer(reducer: ActionReducer<any>): ActionReducer<any> {
  return (state, action) => {
    const newState = reducer(state, action);
    console.log("[Local Storage State] ======> ",newState)
    const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(newState), secretKey).toString();
    localStorage.setItem('appState', encryptedState);
    return newState;
  };
}


