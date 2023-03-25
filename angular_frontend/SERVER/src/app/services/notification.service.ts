import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  notification :any
  public activeNotification$:any = new BehaviorSubject<any>({});
  constructor(private toastr: ToastrService) {}

  success(message: string,title:string,config:any) {
    this.toastr.success(message,title,config);
  }

  error(message: string,title:string,config:any) {
    this.toastr.show(message,title,config);
  }

  public setModalNotification(notification){
    this.notification = notification
    console.log(this.notification)
    this.activeNotification$.next(this.notification);
  }

  public getActiveNotification(){
    return this.activeNotification$.asObservable()
  }
}
