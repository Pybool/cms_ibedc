import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { UserState } from '../authentication/state/auth.selector';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class CustomercreationupdateService {
  userState;
  public draft_id$:any = new BehaviorSubject<number>(0);

  constructor(private store: Store<AppState>,private http: HttpClient,private router: Router) { 
    this.userState = this.store.select(UserState);
  }

  getItemByTag(array, draft_tag) {
    return array.find(item => item.draft_tag === draft_tag);
  }

  public setDraftId(id){
    this.draft_id$.next(id);
  }

  public getDraftId(){

    return this.draft_id$.asObservable()
  }

  public fetchDrafts(){
    return this.http.get<any>(`${environment.api}/cms/drafts`)
  }

  public loadDraft(payload){
    let draft = this.getItemByTag(payload.drafts,payload.tag)
    if(draft){
      return of({status:true,data:draft})
    }
    else{
      return of({status:false,data:draft})
    }
    
  }

  saveDraft(payload:any){
    return this.http.post<any>(`${environment.api}/cms/drafts`,payload)
  }

  checkOrCreateNewAwaitingCustomer(payload:any){
    return this.http.post<any>(`${environment.api}/cms/awaiting_customer`,payload)
  }

  updateExistsAwaitingCustomer(payload){
    return this.http.put<any>(`${environment.api}/cms/awaiting_customer`,payload)
  }

  createExistsAwaitingCustomer(payload){
    return this.http.put<any>(`${environment.api}/cms/awaiting_customer`,payload)
  }
}
