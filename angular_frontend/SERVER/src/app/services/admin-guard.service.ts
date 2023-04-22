import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    const adminStatus = this.authService.getAdminStatus();
    if (adminStatus == true) { // replace with the required value and condition
      return true;
    } else {
      this.router.navigate(['/unauthorized']);
      return false;
    }
  }
}


