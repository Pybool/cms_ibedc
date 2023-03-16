
import { UserService } from 'src/app/services/user.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { UserActionTypes, LoadUser, LoadUserSuccess,LoadUserFailure, FetchUsersSuccess, FetchUsersFailure } from './user.actions';
import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
import { UpdateUser } from '../../createuser/models/user';

@Injectable()
export class UserEffects {

  constructor(
    private actions$: Actions,
    private userService: UserService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here

FetchUsersSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.LOAD_USER_SUCCESS),
        tap((data:any) => {
            
            // this.router.navigateByUrl('/admin/users');
        })
    ),
    { dispatch: false }
)

FetchUsersFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.LOAD_USER_FAILURE)
    ),
    { dispatch: false }
)

LoadUserSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.LOAD_USER_SUCCESS),
        tap((signup:any) => {
            // this.router.navigateByUrl('/admin/users');
        })
    ),
    { dispatch: false }
)

LoadUserFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.LOAD_USER_FAILURE)
    ),
    { dispatch: false }
)

FetchUsers$= createEffect(() => 
    this.actions$.pipe(
        ofType(UserActionTypes.FETCH_USERS),
        map((action: LoadUser) => action.payload),
        switchMap(payload => {
            return this.userService.fetchusers().pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new FetchUsersSuccess(response.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetch users")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchUsersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)


LoadUser$= createEffect(() => 
    this.actions$.pipe(
        ofType(UserActionTypes.LOAD_USER),
        map((action: LoadUser) => action.payload),
        switchMap(payload => {
            return this.userService.createUser(payload).pipe(
                map((user) => {
                    console.log(user);
                    if(user.status){
                        user.email = payload.email
                        return new LoadUserSuccess(user.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Could not load user")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new LoadUserFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

// RehydrateLogIn$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.REHYDRATE_LOGIN),
//         map(() => {
//         const user = this.userService.getUserFromLocalStorage();
//           console.log("Rehydration ====> ", user)
//           return new AuthRehydrateSuccess(user);
//         })
//     )
// )

// AuthRehydrateSuccess$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.LOGIN_SUCCESS),
//         tap((user:any) => {
//             localStorage.setItem('token', user.payload.token);
//         })
//     ),
//     { dispatch: false }
// )

// LogInSuccess$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.LOGIN_SUCCESS),
//         tap((user:any) => {
//             localStorage.setItem('token', user.payload.token);
//             this.router.navigateByUrl('/dashboard');
//             this.notificationService.success("Logged in Successfully","CMS Authentication Successful",{titleClass: 'toast-title',
//                                                                                     iconClasses:'toast-success',
//                                                                                     autoDismiss:false});
//         })
//     ),
//     { dispatch: false }
// )

// LogInFailure$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.LOGIN_FAILURE),
//         tap((msg) => {
//             this.notificationService.error("Incorrect credentials supplied!!","CMS Authentication Failure",{titleClass: 'toast-title',
//                                                                                     iconClasses:'toast-error',
//                                                                                     autoDismiss:false});
//           })
//     ),
//     { dispatch: false }
// )

// LogOut$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.LOGOUT),
//         tap((user:any) => {
//             console.log("User token ===>",user)
//             localStorage.removeItem('token');
//             this.router.navigateByUrl('/login');
//         })
//     ),
//     { dispatch: false }
// )

// GetStatus$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.GET_STATUS),
//         map((action: GetStatus) => action),
//         switchMap(payload => {
//             return this.userService.getStatus();
//         })
//     ),
//     { dispatch: false }
// )

// VerifyOtp$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(UserActionTypes.VERIFY_OTP),
//         map((action: VerifyOtp) => action.payload),
//         switchMap(payload => {
//             return this.userService.verifyotp(payload).pipe(
//                 map((user) => {
//                     console.log(user);
//                     return new VerifyOtpSuccess({email: payload.email});
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new VerifyOtpFailure({ error: error }));
//                 })
//             )
            
//         })
//     )
// )

// VerifyOtpSuccess$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.VERIFY_OTP_SUCCESS),
//         tap((user:any) => {
//             this.router.navigateByUrl('/login');
//         })
//     ),
//     { dispatch: false }
// )

// VerifyOtpFailure$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(UserActionTypes.VERIFY_OTP_FAILURE)
//     ),
//     { dispatch: false }
// )
    
    

}