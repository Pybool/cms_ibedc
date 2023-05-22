
import { CustomerService } from 'src/app/services/customer.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { CaadListActionTypes, 
        FetchCaadList, FetchCaadListSuccess, FetchCaadListFailure
        } from './caadlist.actions';

import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
import { CaadService } from 'src/app/services/caad.service';
import { ApproveCaadFailure, ApproveCaadSuccess, CustomerCaadActionTypes } from '../../customerdetails/caad/state/customercaad.actions';

@Injectable()
export class CaadListEffects {

  constructor(
    private actions$: Actions,
    private caadService: CaadService,
    private notificationService: NotificationService
  ) {}
  // effects go here

FetchCaadListFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CaadListActionTypes.FETCH_CAAD_LIST_FAILURE)
    ),
    { dispatch: false }
)

FetchCaadListSuccess$= createEffect(() => 

this.actions$.pipe(
    ofType(CaadListActionTypes.FETCH_CAAD_LIST_SUCCESS),
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
        console.log(data)
    })
),
{ dispatch: false }
)

FetchCaadList$= createEffect(() => 
    this.actions$.pipe(
        ofType(CaadListActionTypes.FETCH_CAAD_LIST),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.caadService.fetchCaadList().pipe(
                map((response:any) => {
                    console.log(response);
                    if(response.status){
                        return new FetchCaadListSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for saving draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchCaadListFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )            
        })
    )
)


ApproveCaad$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerCaadActionTypes.APPROVE_CAAD),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.caadService.caadApproval(payload,1).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        let notification = {type:'success',title:'CAAD Approval Successful!',
                        message:response?.message,
                        subMessage:'...'}
                        this.notificationService.setModalNotification(notification)
                        this.caadService.setCaadSucess(true)
                        return new ApproveCaadSuccess(response) as Action; // cast to Action
                    }
                    else{
                        let notification = {type:'failure',title:'Oops!',
                        message:response?.message,
                        subMessage:'Something went wrong'}
                        this.notificationService.setModalNotification(notification)
                        throw new Error("Server returned false status for fetching draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new ApproveCaadFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )            
        })
    )
)

// RevertCaads$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CaadListActionTypes.LOAD_DRAFT),
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