import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject, of } from 'rxjs';
import { take, timeout } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { UserState } from '../authentication/state/auth.selector';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class BillingService {
  userState
  permission_hierarchy
  billingList;
  billingList$:any = new BehaviorSubject<any>({});
  constructor(private http: HttpClient,private store: Store<AppState>,
    private router: Router) {  this.userState = this.store.select(UserState);}

    setMetadata(){
      this.userState.pipe(
        take(1)
      ).subscribe((user) => {
        this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
        
      });
    }

    swapBillinglist(data){
      this.billingList = data.data
      
      this.billingList$.next(data)
      console.log(this.billingList)
    }
  
    public getbillingList(){
      return this.billingList$.asObservable()
    }

  fetchCustomersBilling(){
    this.setMetadata()
    return this.http.get<any>(`${environment.api}/customers-bills?page=${1}&permission_hierarchy=${this.permission_hierarchy}`).pipe(
      timeout(60000)
    )

  }

  deepSearchBilling(payload){
      return this.http.get<any>(`${environment.api}/search-customers-bills?page=${1}&type=${payload.type}&field=${payload.fieldName}&value=${payload.q[0]}&permission_hierarchy=${this.permission_hierarchy}`).pipe(
        timeout(60000)
      )
    }
  
}
