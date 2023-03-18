import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BasicinformationComponent } from '../basicinformation/basicinformation.component';
import { PaymentsinformationComponent } from './paymentsinformation.component';
import { DataTablesModule } from 'angular-datatables';

const routes:Routes = []

@NgModule({
  declarations: [ PaymentsinformationComponent ],
  imports: [
    CommonModule,
    DataTablesModule,
    RouterModule.forChild(routes),
  ],
})
export class PaymentsinformationModule { }

