import { UserService } from 'src/app/services/user.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { CustomSelectActionTypes, FetchServiceCenters, 
                FetchServiceCentersSuccess, 
                FetchServiceCentersFailure,
                FetchBusinessHubs,
                FetchBusinessHubsSuccess } from './customselect.actions';
import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';

@Injectable()
export class CustomSelectEffects {

  constructor(
    private actions$: Actions,
    private userService: UserService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here


FetchBusinessHubsSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_BUSINESS_HUBS_SUCCESS),
        tap((response:any) => {

        })
    ),
    { dispatch: false }
)

FetchBusinessHubsFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_BUSINESS_HUBS_FAILURE)
    ),
    { dispatch: false }
)

FetchServiceCentersSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_SERVICE_CENTERS_SUCCESS),
        tap((response:any) => {

        })
    ),
    { dispatch: false }
)

FetchServiceCentersFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_SERVICE_CENTERS_FAILURE)
    ),
    { dispatch: false }
)


FetchBusinessHubs$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_BUSINESS_HUBS),
        map((action: FetchBusinessHubs) => action.payload),
        switchMap(payload => {
            console.log("Effects payload ", payload)
            return this.userService.fetchServiceCentersAndBusinessHubs(payload).pipe(
                map((location) => {
                    console.log(location);
                    if(location.status){
                        return new FetchBusinessHubsSuccess(location.data.business_units) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetch")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchServiceCentersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

FetchServiceCenters$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomSelectActionTypes.FETCH_SERVICE_CENTERS),
        map((action: FetchServiceCenters) => action.payload),
        switchMap(payload => {
            console.log("Effects payload ", payload)
            return this.userService.fetchServiceCentersAndBusinessHubs(payload).pipe(
                map((location) => {
                    console.log(location);
                    if(location.status){
                        return new FetchServiceCentersSuccess(location.data.service_centers) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetch")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchServiceCentersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

// RehydrateLogIn$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(CustomSelectActionTypes.REHYDRATE_LOGIN),
//         map(() => {
//         const user = this.userService.getUserFromLocalStorage();
//           console.log("Rehydration ====> ", user)
//           return new AuthRehydrateSuccess(user);
//         })
//     )
// )

// AuthRehydrateSuccess$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(CustomSelectActionTypes.LOGIN_SUCCESS),
//         tap((user:any) => {
//             localStorage.setItem('token', user.payload.token);
//         })
//     ),
//     { dispatch: false }
// )

// LogInSuccess$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(CustomSelectActionTypes.LOGIN_SUCCESS),
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
//         ofType(CustomSelectActionTypes.LOGIN_FAILURE),
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
//         ofType(CustomSelectActionTypes.LOGOUT),
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
//         ofType(CustomSelectActionTypes.GET_STATUS),
//         map((action: GetStatus) => action),
//         switchMap(payload => {
//             return this.userService.getStatus();
//         })
//     ),
//     { dispatch: false }
// )

// VerifyOtp$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CustomSelectActionTypes.VERIFY_OTP),
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
//         ofType(CustomSelectActionTypes.VERIFY_OTP_SUCCESS),
//         tap((user:any) => {
//             this.router.navigateByUrl('/login');
//         })
//     ),
//     { dispatch: false }
// )

// VerifyOtpFailure$= createEffect(() => 

//     this.actions$.pipe(
//         ofType(CustomSelectActionTypes.VERIFY_OTP_FAILURE)
//     ),
//     { dispatch: false }
// )
    
    

}