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
import { NotificationmodalComponent } from './ui/notificationmodal/notificationmodal.component';
import { LocationsComponent } from './pages/locations/locations.component';
import { AdminGuard } from './services/admin-guard.service';
import { AuthGuard } from './services/auth-guard.service';
import { UnauthorizedComponent } from './unauthorized/unauthorized.component';

const routes: Routes = [
                        { path:'cms/web/login', component:LoginComponent},
                        { path:'unauthorized', component:UnauthorizedComponent},
                        { path:'admin/users', component:UsersComponent, canActivate: [AdminGuard]},
                        { path:'dashboard',component: DashboardComponent , canActivate: [AuthGuard]},
                        { path:'customers/prepaid', component:CustomersComponent, canActivate: [AuthGuard]},
                        { path:'customers/postpaid', component:PostpaidcustomersComponent, canActivate: [AuthGuard]},
                        { path:'cms/customers/crmd', component:CrmdComponent, canActivate: [AuthGuard]},
                        { path:'cms/caadlist', component:CaadlistComponent, canActivate: [AuthGuard]},
                        { path:'admin/locations', component:LocationsComponent, canActivate: [AdminGuard]},
                        { path:'cms/notification/modal', component:NotificationmodalComponent, canActivate: [AuthGuard]},
                        { path:'cms/customers/billing', component:BillingComponent, canActivate: [AuthGuard]},
                        { path:'cms/customers/ecmi/payments', component:PaymentsComponent, canActivate: [AuthGuard]},
                        { path:'cms/customers/ems/payments', component:PaymentsemsComponent, canActivate: [AuthGuard]},
                        { path:'cms/today/prepaid/collections', component:TodaycollectionsecmiComponent, canActivate: [AuthGuard]},
                        { path:'cms/today/postpaid/collections', component:TodaycollectionsemsComponent, canActivate: [AuthGuard]},

                        
                        {
                          path: 'customer/information',
                          loadChildren: () =>
                            import('./pages/customerdetails/customermain/customermain.module').then((m) => m.CustomermainModule),
                          canActivate: [AuthGuard]
                            
                        },
                        {
                          path: 'admin/configurations',
                          loadChildren: () =>
                            import('./pages/configurations/configurations.module').then((m) => m.ConfigurationsModule),
                          canActivate: [AdminGuard]
                        }
                      ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
