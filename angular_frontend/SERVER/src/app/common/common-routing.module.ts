import { CommonComponent } from '../common/common.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from '../authentication/login/login.component';
// import { CustomermainComponent } from './pages/customerdetails/customermain/customermain.component';
import { CustomersComponent } from '../pages/customersmodule/prepaidcustomers/customers.component';
import { DashboardComponent } from '../pages/dashboard/dashboard.component';

const routes: Routes = [
                        { path:'web/login', component:LoginComponent},
                        { path:'dashboard',component: DashboardComponent },
                        { path:'customers', component:CustomersComponent},
                        {
                          path: 'customer/information',
                          loadChildren: () =>
                            import('../pages/customerdetails/customermain/customermain.module').then((m) => m.CustomermainModule),
                            
                        },];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CommonRoutingModule { }
