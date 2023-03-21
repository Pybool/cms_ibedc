import { NgModule } from '@angular/core';
import { DashboardComponent } from '../pages/dashboard/dashboard.component';
import { CustomersComponent } from '../pages/customersmodule/prepaidcustomers/customers.component';
import { LoginComponent } from '../authentication/login/login.component';
import { ResetpasswordComponent } from '../authentication/resetpassword/resetpassword.component';

import { CustomercreationComponent } from '../pages/customercreation/customercreation.component';
import { CustomerupdateComponent } from '../pages/customerupdate/customerupdate.component';
import { ApprovalboardComponent } from '../pages/approvalboard/approvalboard.component';
import { CommonModule } from '@angular/common';
import { CommonRoutingModule } from './common-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { CommonComponent } from './common.component';


@NgModule({
  declarations: [
    CommonComponent,
    DashboardComponent,
    CustomersComponent,
    LoginComponent,
    ResetpasswordComponent,
    CustomercreationComponent,
    CustomerupdateComponent,
    ApprovalboardComponent,],
  imports: [

    CommonModule,
    CommonRoutingModule,
  ],
  exports: [CommonRoutingModule]
})
export class CommonComponentModule { }
