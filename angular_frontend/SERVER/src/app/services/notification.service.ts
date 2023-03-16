import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  constructor(private toastr: ToastrService) {}

  success(message: string,title:string,config:any) {
    this.toastr.success(message,title,config);
  }

  error(message: string,title:string,config:any) {
    this.toastr.show(message,title,config);
  }
}
