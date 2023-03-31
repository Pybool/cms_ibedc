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

  searchPaymentsHistory(payload){
    return this.http.get<any>(`${environment.api}/search-customers-${payload?.type}-payments?field=${payload?.field}&value=${payload?.value}&type=searchbar&permission_hierarchy=${this.permission_hierarchy}`)
  }

  searchDatePaymentsHistory(payload){
    return this.http.get<any>(`${environment.api}/search-customers-${payload?.type}-payments?start_date=${payload?.start_date}&end_date=${payload?.end_date}&type=datewidget&permission_hierarchy=${this.permission_hierarchy}`)
  }
}


// # http://192.168.15.161:8000/api/v1/search-customers-ems-payments?field=PaymentID&value=D15D142D-1F71-E611-940B-9C8E9967C125&type=searchbar&permission_hierarchy=Service Center
// # http://192.168.15.161:8000/api/v1/search-customers-ems-payments?field=accountno&value=12/06/06/1566-01&type=searchbar&permission_hierarchy=Service Center
// # http://192.168.15.161:8000/api/v1/search-customers-ems-payments?start_date=2021-03-04&end_date=2022-09-05&type=datewidget&permission_hierarchy=Service Center
