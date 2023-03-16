
import { CustomerService } from 'src/app/services/customer.service';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { CustomerCreationActionTypes, 
        SaveDraft, FetchDrafts, FetchDraftsFailure,
        SaveDraftSuccess, FetchDraftsSuccess,
        SaveDraftFailure,
        LoadDraftSuccess,
        LoadDraftFailure} from './customercreation.actions';

import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
import { CustomercreationupdateService } from 'src/app/services/customercreationupdate.service';
// import { UpdateUser } from '../../createuser/models/user';

@Injectable()
export class CustomerCreationEffects {

  constructor(
    private actions$: Actions,
    private customersService: CustomerService,
    private customercreationupdateService: CustomercreationupdateService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here


SaveDraftFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.SAVE_DRAFT_FAILURE)
    ),
    { dispatch: false }
)

SaveDraftSuccess$= createEffect(() => 

this.actions$.pipe(
    ofType(CustomerCreationActionTypes.SAVE_DRAFT_SUCCESS),
    tap((data:any) => {
        this.customercreationupdateService.setDraftId(data.payload.id)
    })
),
{ dispatch: false }
)

FetchDraftsFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.FETCH_DRAFTS_FAILURE)
    ),
    { dispatch: false }
)

FetchDraftsSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.FETCH_DRAFTS_SUCCESS),
        tap((data:any) => {
        })
    ),
    { dispatch: false }
    )

SaveDraft$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.SAVE_DRAFT),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customercreationupdateService.saveDraft(payload).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new SaveDraftSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for saving draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new SaveDraftFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)


FetchDrafts$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.FETCH_DRAFTS),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customercreationupdateService.fetchDrafts().pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new FetchDraftsSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetching draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchDraftsFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

LoadDrafts$= createEffect(() => 
    this.actions$.pipe(
        ofType(CustomerCreationActionTypes.LOAD_DRAFT),
        map((action: any) => action.payload),
        switchMap(payload => {
            return this.customercreationupdateService.loadDraft(payload).pipe(
                map((response) => {
                    console.log(response);
                    if(response.status){
                        return new LoadDraftSuccess(response) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for fetching draft")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new LoadDraftFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)
}