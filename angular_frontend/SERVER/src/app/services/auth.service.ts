import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { Observable } from 'rxjs';
import { User, UserModel } from '../authentication/models/user';
import * as CryptoJS from 'crypto-js';
import { environment } from 'src/environments/environment';
import {Router} from '@angular/router'; // import router from angular router

const secretKey = environment.AES_SECRET_KEY;

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  static authEmitter = new EventEmitter<boolean>();

  accessToken = this.getUserFromLocalStorage().token;

  constructor(private http: HttpClient,private router: Router,) {
  }

  getAdminStatus(){
    return this.getUserFromLocalStorage().is_admin;
  }

  newUser(body: any) {
    return this.http.post(`${environment.api}/newUser`, body);
  }

  verifyotp(body: any) {
    return this.http.post(`${environment.api}/signup_verify_otp`, body);
  }

  login(body: any): Observable<any> {
    return this.http.post(`${environment.api}/login`, body);
    
  }

  getStatus(): Observable<User> {
    const url = `${environment.api}/status`;
    return this.http.get<User>(url);
  }

  authenticatorLogin(body: any) {
    return this.http.post(`${environment.api}/auth/two-factor`, body, {withCredentials: true});
  }

  googleLogin(body: any) {
    return this.http.post(`${environment.api}/auth/oauth-google`, body, {withCredentials: true});
  }

  user() {
    return this.http.get(`${environment.api}/authenticated_user`);
  }

  getToken(): string {
    return localStorage.getItem('token');
  }

  refresh() {
    return this.http.get(`${environment.api}/refreshtoken`,  {withCredentials: true});
  }

  logout() {
    localStorage.removeItem('appState');
    this.router.navigateByUrl("/cms/web/login")
    
  }

  formatUser(data: any) {
    
    const user = new UserModel(
    data.email,
    data.token,
    data.action_id,
    data.active,
    data.avatar,
    data.bio,
    data.bucode,
    data.business_unit,
    data.can_approve,
    data.can_approve_caad,
    data.can_create_customer,
    data.created_at,
    data.enable_2fa,
    data.firstname,
    data.id,
    data.ig_handle,
    data.is_regularuser,
    data.is_superuser,
    data.is_verified_account,
    data.last_login,
    data.lastname,
    data.manage_2fa,
    data.otp,
    data.otp_expires_at,
    data.permission_hierarchy,
    data.phone1,
    data.password,
    data.position,
    data.region,
    data.secret_code_2fa,
    data.servicecenter,
    data.slug,
    data.suspend_user,
    data.twitter_handle,
    data.updated_at,
    data.user_type,
    data.username,
    );
    return user.getUser();
  }

  setUserInLocalStorage(user: User) {
    console.log("store it ====> ",user)
    this.accessToken = user.token
    console.log(this.accessToken)
    const encryptedState = CryptoJS.AES.encrypt(JSON.stringify(user), secretKey).toString();
    localStorage.setItem('appState', encryptedState);
  }

  getUserFromLocalStorage(): any {
    const savedState = localStorage.getItem('appState');
    if (savedState) {
      const bytes = CryptoJS.AES.decrypt(savedState, secretKey);
      const userData = JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
      const user = userData.user
      return user;
    }
    return {};
  }


}





