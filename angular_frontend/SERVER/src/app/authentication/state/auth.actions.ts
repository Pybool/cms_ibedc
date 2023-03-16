import { Action } from '@ngrx/store';


export enum AuthActionTypes {
  SIGNUP = '[Auth] Signup',
  SIGNUP_SUCCESS = '[Auth] Signup Success',
  SIGNUP_FAILURE = '[Auth] Signup Failure',

  LOGIN = '[Auth] Login',
  LOGIN_SUCCESS = '[Auth] Login Success',
  LOGIN_FAILURE = '[Auth] Login Failure',
  REHYDRATE_LOGIN ='[Auth] Rehydrate',
  AUTH_REHYDRATE_SUCCESS = "[Auth] Rehydrate Success",
  LOGOUT = '[Auth] Logout',

  VERIFY_OTP = '[Auth] Verifyotp',
  VERIFY_OTP_SUCCESS = '[Auth] Verifyotp Success',
  VERIFY_OTP_FAILURE = '[Auth] Verifyotp Failure',

  GET_STATUS = '[Auth] GetStatus'
}
export class SignUp implements Action {
    readonly type = AuthActionTypes.SIGNUP;
    constructor(public payload: any) {}
  }
export class SignUpSuccess implements Action {
    readonly type = AuthActionTypes.SIGNUP_SUCCESS;
    constructor(public payload: any) {}
  }
export class SignUpFailure implements Action {
    readonly type = AuthActionTypes.SIGNUP_FAILURE;
    constructor(public payload: any) {}
  }
  export class RehydrateLogIn implements Action {
    readonly type = AuthActionTypes.REHYDRATE_LOGIN;
    constructor(public payload: any) {}
  }

  export class AuthRehydrateSuccess implements Action {
    readonly type = AuthActionTypes.AUTH_REHYDRATE_SUCCESS;
    constructor(public payload: any) {}
  }

export class LogIn implements Action {
    readonly type = AuthActionTypes.LOGIN;
    constructor(public payload: any) {}
  }
export class LogInSuccess implements Action {
    readonly type = AuthActionTypes.LOGIN_SUCCESS;
    constructor(public payload: any) {}
  }
export class LogInFailure implements Action {
    readonly type = AuthActionTypes.LOGIN_FAILURE;
    constructor(public payload: any) {}
  }
export class LogOut implements Action {
    readonly type = AuthActionTypes.LOGOUT;
  }
export class VerifyOtp implements Action {
    readonly type = AuthActionTypes.VERIFY_OTP;
    constructor(public payload: any) {}
  }
export class VerifyOtpSuccess implements Action {
    readonly type = AuthActionTypes.VERIFY_OTP_SUCCESS;
    constructor(public payload: any) {}
  }
export class VerifyOtpFailure implements Action {
    readonly type = AuthActionTypes.VERIFY_OTP_FAILURE;
    constructor(public payload: any) {}
  }

export class GetStatus implements Action {
    readonly type = AuthActionTypes.GET_STATUS;
  }
    
export type All =
  | SignUp
  | SignUpSuccess
  | SignUpFailure
  | LogIn
  | LogOut
  | LogInSuccess
  | LogInFailure
  | VerifyOtp
  | VerifyOtpSuccess
  | VerifyOtpFailure
  | RehydrateLogIn
  | AuthRehydrateSuccess
  | GetStatus;


    