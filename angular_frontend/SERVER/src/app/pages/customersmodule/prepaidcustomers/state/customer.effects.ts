
import { CustomerService } from 'src/app/services/customer.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { CustomerActionTypes, 
        LoadEmsCustomer, 
        FetchEcmiCustomers,
        FetchEmsCustomers, 
        FetchEcmiCustomersSuccess,
        FetchEcmiCustomersFailure,
        FetchEmsCustomersSuccess,
        FetchEmsCustomersFailure, 
        DeepFetchEcmiCustomersSuccess,
        DeepFetchEcmiCustomersFailure,
        LoadEmsCustomersuccess,
        LoadEmsCustomerFailure} from './customer.actions';

import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
// import { UpdateUser } from '../../createuser/models/user';

@Injectable()
export class CustomerEffects {

  constructor(
    private actions$: Actions,
    private customersService: CustomerService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here

FetchEcmiCustomersSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.FETCH_ECMI_CUSTOMERS_SUCCESS),
        tap((data:any) => {
            
        })
    ),
    { dispatch: false }
)

FetchEcmiCustomersFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.FETCH_ECMI_CUSTOMERS_FAILURE)
    ),
    { dispatch: false }
)

FetchEmsCustomersSuccess$= createEffect(() => 

this.actions$.pipe(
    ofType(CustomerActionTypes.FETCH_EMS_CUSTOMERS_SUCCESS),
    tap((data:any) => {
        
    })
),
{ dispatch: false }
)

FetchEmsCustomersFailure$= createEffect(() => 

this.actions$.pipe(
    ofType(CustomerActionTypes.FETCH_EMS_CUSTOMERS_FAILURE)
),
{ dispatch: false }
)




DeepFetchEcmiCustomersSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_SUCCESS),
        tap((data:any) => {
            
        })
    ),
    { dispatch: false }
)

DeepFetchEcmiCustomersFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS_FAILURE)
    ),
    { dispatch: false }
)

DeepFetchEmsCustomersSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.DEEP_FETCH_EMS_CUSTOMERS_SUCCESS),
        tap((data:any) => {
            
        })
    ),
    { dispatch: false }
)

DeepFetchEmsCustomersFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.DEEP_FETCH_EMS_CUSTOMERS_FAILURE)
    ),
    { dispatch: false }
)

LoadEmsCustomerSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.LOAD_EMS_CUSTOMER_SUCCESS),
        tap((signup:any) => {
            // this.router.navigateByUrl('/admin/users');
        })
    ),
    { dispatch: false }
)

LoadEmsCustomerFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerActionTypes.LOAD_EMS_CUSTOMER_FAILURE)
    ),
    { dispatch: false }
)

FetchEcmiCustomers$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerActionTypes.FETCH_ECMI_CUSTOMERS),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customersService.fetchcustomers('prepaid').pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new FetchEcmiCustomersSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetch Ecmi Customers")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchEcmiCustomersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)


FetchEmsCustomers$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerActionTypes.FETCH_EMS_CUSTOMERS),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customersService.fetchcustomers('postpaid').pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new FetchEmsCustomersSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetch Ems Customers")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchEmsCustomersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

DeepFetchEcmiCustomers$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerActionTypes.DEEP_FETCH_ECMI_CUSTOMERS),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customersService.deepFetchCustomers(payload).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        this.customersService.swapCustomerlist(response)
                        return new DeepFetchEcmiCustomersSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Data was not fetched from server")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new DeepFetchEcmiCustomersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

// DeepFetchEmsCustomers$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CustomerActionTypes.DEEP_FETCH_EMS_CUSTOMERS),
//         map((action: any) => action.payload),
//         switchMap(payload => {
//             return this.customersService.deepFetchCustomers(payload).pipe(
//                 map((response) => {
//                     if(response.status){
//                         return new DeepFetchEmsCustomersSuccess(response) as Action; // cast to Action
//                     }
//                     else{
//                         throw new Error("Server returned false status for fetch Ems Customers")
//                     }
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new DeepFetchEmsCustomersFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
//                 })
//             )
//         })
//     )
// )

// LoadEmsCustomers$= createEffect(() => 
//     this.actions$.pipe(
//         ofType(CustomerActionTypes.LOAD_EMS_CUSTOMER),
//         map((action: any) => action.payload),
//         switchMap(payload => {
//             return this.customersService.fetchSinglecustomer(payload).pipe(
//                 map((response) => {
//                     console.log(response);
//                     if(response.status){
//                         return new LoadEmsCustomersuccess(response) as Action; // cast to Action
//                     }
//                     else{
//                         throw new Error("Server returned false status for fetch Ems Customers")
//                     }
//                 }),
//                 catchError((error) => {
//                     console.log(error);
//                     return of(new LoadEmsCustomerFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
//                 })
//             )
//         })
//     )
// )

}