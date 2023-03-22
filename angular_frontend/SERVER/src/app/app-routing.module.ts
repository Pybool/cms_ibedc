import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './authentication/login/login.component';
import { CaadlistComponent } from './pages/caadlist/caadlist.component';
import { ConfigurationsComponent } from './pages/configurations/configurations.component';
import { CrmdComponent } from './pages/crmd/crmd.component';
// import { CustomermainComponent } from './pages/customerdetails/customermain/customermain.component';
import { CustomersComponent } from './pages/customersmodule/prepaidcustomers/customers.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PostpaidcustomersComponent } from './pages/customersmodule/postpaidcustomers/postpaidcustomers.component';
import { UsersComponent } from './pages/user/users/users.component';
import { BillingComponent } from './pages/billing/billing.component';
import { PaymentsComponent } from './pages/payments/payments.component';
import { PaymentsemsComponent } from './pages/paymentsems/paymentsems.component';
import { TodaycollectionsecmiComponent } from './pages/todaycollectionsecmi/todaycollectionsecmi.component';
import { TodaycollectionsemsComponent } from './pages/todaycollectionsems/todaycollectionsems.component';

const routes: Routes = [
                        { path:'cms/web/login', component:LoginComponent},
                        { path:'admin/users', component:UsersComponent},
                        { path:'dashboard',component: DashboardComponent },
                        { path:'customers/prepaid', component:CustomersComponent},
                        { path:'customers/postpaid', component:PostpaidcustomersComponent},
                        { path:'cms/customers/crmd', component:CrmdComponent},
                        { path:'cms/caadlist', component:CaadlistComponent},
                        { path:'cms/customers/billing', component:BillingComponent},
                        { path:'cms/customers/ecmi/payments', component:PaymentsComponent},
                        { path:'cms/customers/ems/payments', component:PaymentsemsComponent},
                        { path:'cms/today/prepaid/collections', component:TodaycollectionsecmiComponent},
                        { path:'cms/today/postpaid/collections', component:TodaycollectionsemsComponent},

                        
                        {
                          path: 'customer/information',
                          loadChildren: () =>
                            import('./pages/customerdetails/customermain/customermain.module').then((m) => m.CustomermainModule),
                            
                        },
                        {
                          path: 'admin/configurations',
                          loadChildren: () =>
                            import('./pages/configurations/configurations.module').then((m) => m.ConfigurationsModule),
                            
                        }
                      ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
