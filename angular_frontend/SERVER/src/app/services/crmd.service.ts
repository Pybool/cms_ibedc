import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject } from 'rxjs';
import { environment } from 'src/environments/environment';
import { UserState } from '../authentication/state/auth.selector';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class CrmdService {
  userState:any;
  awaitingCustomers:any = []
  awaitingCustomers$:any = new BehaviorSubject<any>([]);

  constructor(private store: Store<AppState>,private http: HttpClient,private router: Router) { 
    this.userState = this.store.select(UserState);
  }

  public cacheAwaitingCustomers(awaitingCustomers){
    this.awaitingCustomers = awaitingCustomers
    this.awaitingCustomers$.next(this.awaitingCustomers);
  }

  public getCacheAwaitingCustomers(){
    return this.awaitingCustomers$.asObservable()
  }


  fetchAwaitingCustomers(payload:any){
    if(this.awaitingCustomers.length == 0){
      return this.http.get<any>(`${environment.api}/cms/awaiting/customers?status=${payload?.status}`)
    }
    return this.getCacheAwaitingCustomers()
    
  }

  performAwaitingCustomerAction(payload:any){
    return this.http.put<any>(`${environment.api}/cms/awaiting/customers`,payload)
    
  }
}
