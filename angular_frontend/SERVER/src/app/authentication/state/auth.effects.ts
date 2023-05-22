import { NotificationService } from './../../services/notification.service';
import { AuthService } from './../../services/auth.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { AuthActionTypes, LogIn, LogInFailure, LogInSuccess,SignUp,SignUpFailure,
  SignUpSuccess,VerifyOtp, VerifyOtpFailure, VerifyOtpSuccess, LogOut, GetStatus, RehydrateLogIn, AuthRehydrateSuccess 
} from './auth.actions';
import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import Swal from 'sweetalert2';

@Injectable()
export class AuthEffects {

  constructor(
    private actions$: Actions,
    private authService: AuthService,
    private router: Router,
    private notificationService: NotificationService
  ) {}

  // effects go here

// SignUp$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(AuthActionTypes.SIGNUP),
//         map((action: SignUp) => action.payload),
//         switchMap(payload => {
//             return this.authService.register(payload).pipe(
//                 map((signup:any) => {
//                     console.log("Enter this Temporary otp ==> ",signup.temporary_otp_here);
//                     if(signup.status){
                      
//                         return new SignUpSuccess({token: signup.temporary_otp_here, email: payload.email});
//                     }
//                     else{throw new Error("Server returned false status for registration")}
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new SignUpFailure({ error: error }));
//                 })
//             )
            
//         })
//     )
// )

SignUpSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.SIGNUP_SUCCESS),
        tap((signup:any) => {
            this.router.navigateByUrl('/verify-otp');
        })
    ),
    { dispatch: false }
)

SignUpFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.SIGNUP_FAILURE)
    ),
    { dispatch: false }
)


LogIn$= createEffect(() => 
    this.actions$.pipe(
        ofType(AuthActionTypes.LOGIN),
        map((action: LogIn) => action.payload),
        switchMap(payload => {
            return this.authService.login(payload).pipe(
                map((user) => {
                    console.log(user);
                    if(user.status){
                      user.email = payload.email
                      const authuser:any = user.data
                       this.authService.setUserInLocalStorage(authuser);
                        return new LogInSuccess(user.data);
                    }
                    else{throw new Error("Server returned false status for login")}
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new LogInFailure({ error: error }));
                })
            )
            
        })
    )
)

RehydrateLogIn$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.REHYDRATE_LOGIN),
        map(() => {
        const user = this.authService.getUserFromLocalStorage();
          console.log("Rehydration ====> ", user)
          return new AuthRehydrateSuccess(user);
        })
    )
)

AuthRehydrateSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.LOGIN_SUCCESS),
        tap((user:any) => {
            localStorage.setItem('token', user.payload.token);
        })
    ),
    { dispatch: false }
)

LogInSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.LOGIN_SUCCESS),
        tap((user:any) => {
            localStorage.setItem('token', user.payload.token);
            this.router.navigateByUrl('/dashboard');
            
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: 'Logged in Successfully!',
                text:'CMS Authentication Successful!!',
                showConfirmButton: false,
                timer: 1500
                })
        })
    ),
    { dispatch: false }
)

LogInFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.LOGIN_FAILURE),
        tap((msg) => {
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: 'CMS Authentication Failure',
                text:'Incorrect credentials supplied!!',
                showConfirmButton: false,
                timer: 1500
                })
          })
    ),
    { dispatch: false }
)

LogOut$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.LOGOUT),
        tap((user:any) => {
            console.log("User token ===>",user)
            localStorage.removeItem('token');
            this.router.navigateByUrl('/login');
        })
    ),
    { dispatch: false }
)

GetStatus$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.GET_STATUS),
        map((action: GetStatus) => action),
        switchMap(payload => {
            return this.authService.getStatus();
        })
    ),
    { dispatch: false }
)

VerifyOtp$= createEffect(() => 
    this.actions$.pipe(
        ofType(AuthActionTypes.VERIFY_OTP),
        map((action: VerifyOtp) => action.payload),
        switchMap(payload => {
            return this.authService.verifyotp(payload).pipe(
                map((user) => {
                    console.log(user);
                    return new VerifyOtpSuccess({email: payload.email});
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new VerifyOtpFailure({ error: error }));
                })
            )
            
        })
    )
)

VerifyOtpSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.VERIFY_OTP_SUCCESS),
        tap((user:any) => {
            this.router.navigateByUrl('/login');
        })
    ),
    { dispatch: false }
)

VerifyOtpFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(AuthActionTypes.VERIFY_OTP_FAILURE)
    ),
    { dispatch: false }
)
    
    

}