import { UpdateUser } from '../createuser/models/user';
import { UserService } from 'src/app/services/user.service';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { UserActionTypes, CreateNewUser, CreateUserSuccess, CreateUserFailure,UpdateExistingUser, UpdateUserSuccess } from './createuser.actions';
import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';

@Injectable()
export class CreateUserEffects {

  constructor(
    private actions$: Actions,
    private userService: UserService,
    private router: Router,
    private notificationService: NotificationService,
    private route: ActivatedRoute,
  ) {}
  // effects go here


CreateUserSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.CREATE_USER_SUCCESS),
        tap((signup:any) => {
            // this.router.navigate(['/admin/users']);
        })
    ),
    { dispatch: false }
)

CreateUserFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.CREATE_USER_FAILURE)
    ),
    { dispatch: false }
)


CreateNewUser$= createEffect(() => 
    this.actions$.pipe(
        ofType(UserActionTypes.CREATE_NEW_USER),
        map((action: CreateNewUser) => action.payload),
        switchMap(payload => {
            return this.userService.createUser(payload).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        response.email = payload.email
                        this.notificationService.success(response.message,'Creation successfull',{})
                        return new CreateUserSuccess(response.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for login")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new CreateUserFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

UpdateUserSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.UPDATE_USER_SUCCESS),
        tap((signup:any) => {
         
        })
    ),
    { dispatch: false }
)

UpdateUserFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(UserActionTypes.UPDATE_USER_FAILURE)
    ),
    { dispatch: false }
)


UpdateUser$= createEffect(() => 
    this.actions$.pipe(
        ofType(UserActionTypes.UPDATE_EXISTING_USER),
        map((action: UpdateExistingUser) => action.payload),
        switchMap((payload) => {
            return this.userService.updateUser(payload).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        this.notificationService.success(response.message,'Update successfull',{})
                        return new UpdateUserSuccess(response.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for user update")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new CreateUserFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
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