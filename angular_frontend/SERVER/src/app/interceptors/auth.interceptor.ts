import {Injectable} from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor, HttpErrorResponse
} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError, switchMap} from 'rxjs/operators';
import {AuthService} from "../services/auth.service";
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  refresh = false;

  constructor(private authService: AuthService) {
  }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    console.log(request,this.authService.accessToken)
    const req = request.clone({
      setHeaders: {
        Authorization: `Bearer ${this.authService.accessToken}`
      }
    });

    return next.handle(req).pipe(catchError((err: HttpErrorResponse) => {
      console.log("status code error ===> ",err.status)
      if (err.status === 401 || err.status === 403 && !this.refresh) {
        this.refresh = true;
        return this.authService.refresh().pipe(
          
          switchMap((res: any) => {
            console.log("Refresh token ",res)
            this.authService.accessToken = res.token;

            return next.handle(request.clone({
              setHeaders: {
                Authorization: `Bearer ${this.authService.accessToken}`
              }
            }));
          })
        );
      }
      if (err.status >= 500) {
        // Handle the error here
        // alert('Something went wrong while performing this operation');
      }
      this.refresh = false;
      return throwError(() => err);
    }));
  }
}

// @Injectable()
// export class ErrorInterceptor implements HttpInterceptor {
//   constructor(private router: Router) {}
//   intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

//     return next.handle(request)
//       .catch((response: any) => {
//         if (response instanceof HttpErrorResponse && response.status === 401) {
//           console.log(response);
//         }
//         return Observable.throw(response);
//       });
//   }
// }