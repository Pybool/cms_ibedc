import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import {FormGroup} from "@angular/forms";
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { AppState } from 'src/app/basestore/app.states';
import { User } from '../models/user';
import { LogIn } from '../state/auth.actions';
import { isAuthenticated } from '../state/auth.selector';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  @Output('onLogin') onLogin = new EventEmitter();

  form!: FormGroup;
  user: User = new User();
  getState: Observable<any>;
  errorMessage: string | null;
  Loginpayload:any;
  log;
  
  constructor(
    private store: Store<AppState>
  ) {
    this.getState = this.store.select(isAuthenticated);
  }

  ngOnInit(): void {
    this.getState.subscribe((state) => {
      this.errorMessage = state.errorMessage;
    });
  }

  submit() {
    this.Loginpayload = {email:this.user.email,password:this.user.password}
    this.store.dispatch(new LogIn(this.Loginpayload));
  }

}
