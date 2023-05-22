
import { CustomerService } from 'src/app/services/customer.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { CustomerCaadActionTypes, 
        CreateCaad, ApproveCaad, ApproveCaadFailure,
        CreateCaadSuccess, ApproveCaadSuccess,
        CreateCaadFailure,
        RevertCaadSuccess,
        RevertCaadFailure} from './customercaad.actions';

import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
import { CustomerCaadService } from 'src/app/services/customercaad.service';

@Injectable()
export class CustomerCaadEffects {

  constructor(
    private actions$: Actions,
    private customersService: CustomerService,
    private customerCaadService: CustomerCaadService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here

CreateCaadFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCaadActionTypes.CREATE_CAAD_FAILURE)
    ),
    { dispatch: false }
)

CreateCaadSuccess$= createEffect(() => 

this.actions$.pipe(
    ofType(CustomerCaadActionTypes.CREATE_CAAD_SUCCESS),
    tap((data:any) => {
        
    })
),
{ dispatch: false }
)

ApproveCaadFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCaadActionTypes.APPROVE_CAAD_FAILURE)
    ),
    { dispatch: false }
)

ApproveCaadSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCaadActionTypes.APPROVE_CAAD_SUCCESS),
        tap((data:any) => {
        })
    ),
    { dispatch: false }
    )

CreateCaad$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerCaadActionTypes.CREATE_CAAD),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customerCaadService.createCaad(payload).pipe(
                map((response:any) => {
                    console.log(response);
                    if(response.status){
                        let notification = {type:'success',title:'CAAD Creation Successful!',
                        message:response?.message,
                        subMessage:'...'}
                        this.notificationService.setModalNotification(notification)
                        return new CreateCaadSuccess(response) as Action; // cast to Action
                    }
                    else{
                        let notification = {type:'failure',title:'CAAD Creation Failure!',
                        message:response?.message,
                        subMessage:'...'}
                        this.notificationService.setModalNotification(notification)
                        throw new Error("Server returned false status for saving draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new CreateCaadFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )            
        })
    )
)


// ApproveCaad$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CustomerCaadActionTypes.APPROVE_CAAD),
//         map((action: any) => action.payload),
//         switchMap(payload => {
//             return this.customerCaadService.approveCaad().pipe(
//                 map((response) => {
//                     console.log(response);
//                     if(response.status){
//                         return new ApproveCaadSuccess(response) as Action; // cast to Action
//                     }
//                     else{
//                         throw new Error("Server returned false status for fetching draft")
//                     }
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new ApproveCaadFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
//                 })
//             )            
//         })
//     )
// )

// RevertCaads$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CustomerCaadActionTypes.LOAD_DRAFT),
//         map((action: any) => action.payload),
//         switchMap(payload => {
//             return this.customerCaadService.RevertCaad(payload).pipe(
//                 map((response) => {
//                     console.log(response);
//                     if(response.status){
//                         return new RevertCaadSuccess(response) as Action; // cast to Action
//                     }
//                     else{
//                         throw new Error("Server returned false status for fetching draft")
//                     }
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new RevertCaadFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
//                 })
//             )
            
            
//         })
//     )
// )
}