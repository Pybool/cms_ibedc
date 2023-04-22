import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { GetStatus } from '../authentication/state/auth.actions';
import { AppState, selectAuthState } from '../basestore/app.states';

import { AuthService } from './auth.service';

@Injectable()
export class AuthGuard implements CanActivate {
  getState: Observable<any>;
  constructor(
    public auth: AuthService,
    public router: Router,
    private store: Store<AppState>
  ) {this.getState = this.store.select(selectAuthState);}
  canActivate(): boolean {
    this.getState.subscribe((state) => {
      console.log("Guard data =====> ", state)
    });
    
    if (!this.auth.getToken()) {
      this.router.navigateByUrl('/login');
      return false;
    }
    return true;
  }
}