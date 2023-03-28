// import {  } from '../models/location';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of ,Observable} from "rxjs";
import { LocationActionTypes, FetchLocations,FetchLocationsSuccess,FetchLocationsFailure, CreateLocationsFailure, CreateLocationsSuccess } from './location.actions';
import { map,catchError, filter, switchMap, tap, mergeMap } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { Action } from '@ngrx/store';
import { LocationService } from 'src/app/services/location.service';

@Injectable()
export class LocationsEffects {

  constructor(
    private actions$: Actions,
    private locationService: LocationService,
    private router: Router,
    private notificationService: NotificationService
  ) {}
  // effects go here


FetchLocationsSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(LocationActionTypes.FETCH_LOCATIONS_SUCCESS),
        tap((data:any) => {
        })
    ),
    { dispatch: false }
)

FetchLocationsFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(LocationActionTypes.FETCH_LOCATIONS_FAILURE)
    ),
    { dispatch: false }
)

CreateocationsSuccess$= createEffect(() => 

    this.actions$.pipe(
        ofType(LocationActionTypes.CREATE_LOCATIONS_SUCCESS),
        tap((data:any) => {
        })
    ),
    { dispatch: false }
)

CreateocationsFailure$= createEffect(() => 

    this.actions$.pipe(
        ofType(LocationActionTypes.CREATE_LOCATIONS_FAILURE)
    ),
    { dispatch: false }
)


FetchLocations$= createEffect(() => 
    this.actions$.pipe(
        ofType(LocationActionTypes.FETCH_LOCATIONS),
        switchMap(() => {
            return this.locationService.getLocations().pipe(
                map((response) => {
                    if(response.status){
                        return new FetchLocationsSuccess(response.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false status for login")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new FetchLocationsFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)

createLocations$= createEffect(() => 
    this.actions$.pipe(
        ofType(LocationActionTypes.CREATE_LOCATIONS),
        switchMap((payload:any) => {
            return this.locationService.createLocation(payload?.payload).pipe(
                map((response) => {
                    if(response.status){
                        return new CreateLocationsSuccess(response.data) as Action; // cast to Action
                    }
                    else{
                        throw new Error("Server returned false")
                    }
                }),
                catchError((error) => {
                    console.log(error);
                    return of(new CreateLocationsFailure({ error: error })) as Observable<Action>; // cast to Observable<Action>
                })
            )
            
            
        })
    )
)
 }
