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
export class LocationService {

  constructor(private store: Store<AppState>,private http: HttpClient,private router: Router) { }

  getLocations(){
    return this.http.get<any>(`${environment.api}/cms/admin/locations?cuid=${21}`)
  }

  getSingleLocation(id){
    this.store
  }

  createLocation(payload){
    return this.http.post<any>(`${environment.api}/cms/admin/locations`,payload)
  }
}
