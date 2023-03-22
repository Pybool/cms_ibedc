import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { of } from 'rxjs';
import { take } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { UserState } from '../authentication/state/auth.selector';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class PaymentsService {

  userState
  permission_hierarchy
  constructor(private http: HttpClient,private store: Store<AppState>,
    private router: Router) {  this.userState = this.store.select(UserState);}

    setMetadata(){
      this.userState.pipe(
        take(1)
      ).subscribe((user) => {
        this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
        
      });
    }

  fetchCustomersPayments(){
    this.setMetadata()
    return this.http.get<any>(`${environment.api}/customers-ecmi-payments?page=${1}&permission_hierarchy=${this.permission_hierarchy}`)
  }

  fetchEmsCustomersPayments(){
    this.setMetadata()
    return this.http.get<any>(`${environment.api}/customers-ems-payments?page=${1}&permission_hierarchy=${this.permission_hierarchy}`)
  }

  fetchTodayCollectionsEcmi(){
    this.setMetadata()
    return this.http.get<any>(`${environment.api}/todaycollections-ecmi?page=${1}&permission_hierarchy=${this.permission_hierarchy}`)
  }

  fetchTodayCollectionsEms(){
    this.setMetadata()
    return this.http.get<any>(`${environment.api}/todaycollections-ems?page=${1}&permission_hierarchy=${this.permission_hierarchy}`)
  }
}
