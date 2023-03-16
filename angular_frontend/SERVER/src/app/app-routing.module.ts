import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './authentication/login/login.component';
import { CaadlistComponent } from './pages/caadlist/caadlist.component';
import { ConfigurationsComponent } from './pages/configurations/configurations.component';
import { CrmdComponent } from './pages/crmd/crmd.component';
// import { CustomermainComponent } from './pages/customerdetails/customermain/customermain.component';
import { CustomersComponent } from './pages/customers/customers.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { UsersComponent } from './pages/user/users/users.component';

const routes: Routes = [
                        { path:'cms/web/login', component:LoginComponent},
                        { path:'admin/users', component:UsersComponent},
                        { path:'dashboard',component: DashboardComponent },
                        { path:'customers', component:CustomersComponent},
                        { path:'cms/customers/crmd', component:CrmdComponent},
                        { path:'cms/caadlist', component:CaadlistComponent},
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
