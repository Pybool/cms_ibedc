import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BasicinformationComponent } from '../basicinformation/basicinformation.component';
import { PaymentsinformationComponent } from './paymentsinformation.component';

const routes:Routes = []

@NgModule({
  declarations: [ PaymentsinformationComponent ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ],
})
export class PaymentsinformationModule { }

