import { BillinginformationComponent } from './billinginformation.component';
import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BasicinformationComponent } from '../basicinformation/basicinformation.component';

const routes:Routes = []

@NgModule({
  declarations: [ BillinginformationComponent ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ],
})
export class BillinginformationModule { }

