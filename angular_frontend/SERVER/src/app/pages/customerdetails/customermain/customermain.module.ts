import { AssetsinformationComponent } from './../assetsinformation/assetsinformation.component';
import { MeteringinformationComponent } from './../meteringinformation/meteringinformation.component';
import { PaymentsinformationComponent } from './../paymentsinformation/paymentsinformation.component';
import { CustomermainComponent } from './customermain.component';
import { BillinginformationComponent } from './../billinginformation/billinginformation.component';
import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BasicinformationComponent } from '../basicinformation/basicinformation.component';
import { BillinginformationModule } from '../billinginformation/billinginformation.module';
import { PaymentsinformationModule } from '../paymentsinformation/paymentsinformation.module';
import { CaadComponent } from '../caad/caad.component';
import { DataTablesModule } from 'angular-datatables';
import { AuthGuard } from 'src/app/services/auth-guard.service';
import { AdminGuard } from 'src/app/services/admin-guard.service';
// import { CaadModule } from '../caad/caad.module';
//Basic-Information: http://127.0.0.1:4200/customer/information/basic-information?accounttype=postpaid&accountno=20/29/13/1200-01
//Billing-Information: http://127.0.0.1:4200/customer/information/billing-information?accounttype=postpaid&accountno=20/29/13/1200-01&page=7
//Payment-Information: http://127.0.0.1:4200/customer/information/payment-information?accounttype=postpaid&accountno=20/29/13/1200-01&page=1
//Metering-Information: http://127.0.0.1:4200/customer/information/metering-information?accountno=21/31/72/8789-01&accounttype=prepaid
//Assets-Information : http://127.0.0.1:4200/customer/information/assets-information?accountno=12/28/52/1258-01&accounttype=postpaid

const routes: Routes = [{
            path: '',
            component: CustomermainComponent,
            canActivate: [AuthGuard] ,
            children: [
                { path: 'basic-information', component: BasicinformationComponent,canActivate: [AuthGuard] },
                { path: 'billing-information', component: BillinginformationComponent,canActivate: [AuthGuard] },
                { path: 'payment-information', component: PaymentsinformationComponent,canActivate: [AuthGuard] },
                { path: 'metering-information', component: MeteringinformationComponent,canActivate: [AuthGuard] },
                { path: 'assets-information', component: AssetsinformationComponent,canActivate: [AuthGuard] },
                { path: 'caad-information', component: CaadComponent,canActivate: [AuthGuard] },
            ],
          },
          ]

@NgModule({
  declarations: [ CustomermainComponent ],
  imports: [
    CommonModule,
    // CaadModule,
    DataTablesModule,
    BillinginformationModule,
    PaymentsinformationModule,
    RouterModule.forChild(routes),
  ],
})
export class CustomermainModule { }

