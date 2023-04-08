import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class CustomerCaadService {

  constructor(private store: Store<AppState>,
              private http: HttpClient,
              private router: Router
              ){ }

  createCaad(payload:any){
    return this.http.post<any>(`${environment.api}/cms/customer/caad?action=create`,payload)
  }

  approveCaad(payload:any){
    return this.http.put<any>(`${environment.api}/cms/customer/caad?action=approve`,payload)
  }

  revertCaad(payload:any){
    return this.http.put<any>(`${environment.api}/cms/customer/caad?action=revert`,payload)
  }

  updateCaad(payload:any){
    return this.http.put<any>(`${environment.api}/cms/customer/caad?action=update`,payload)
  }

  fetchCaadList(payload:any){
    return this.http.get<any>(`${environment.api}/cms/customer/caad?action=fetch`)
  }

  fetchCaadHistory(payload:any){
    console.group(payload)
    return this.http.get<any>(`${environment.api}/cms/customer/caad?account_no=${payload.accountno}`)
  }
}
