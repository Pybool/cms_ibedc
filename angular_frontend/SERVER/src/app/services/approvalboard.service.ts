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
export class ApprovalBoardService {
  // userState:any;
  // awaitingCustomers:any = []
  // awaitingCustomers$:any = new BehaviorSubject<any>([]);

  constructor(private store: Store<AppState>,private http: HttpClient,private router: Router) { 
    // this.userState = this.store.select(UserState);
  }

  fetchPendingCustomers(action){
      return this.http.get<any>(`${environment.api}/cms/get_edits_status?action=${action}`)
   
  }

  getSingleCustomer(accountno,action){
    return this.http.get<any>(`${environment.api}/cms/get_edits_status?action=${action}&accountno=${accountno}`)
  }


}
