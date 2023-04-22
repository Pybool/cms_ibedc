import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfigurationsComponent } from './configurations.component';
import { RouterModule, Routes } from '@angular/router';
import { CustomersettingsComponent } from './customersettings/customersettings.component';
import { UsersettingsComponent } from './usersettings/usersettings.component';
import { UserSettingsModule } from './usersettings/usersettings.module';
import { AdminGuard } from 'src/app/services/admin-guard.service';

const routes: Routes = [{
  path: '',
  component: ConfigurationsComponent,
  canActivate: [AdminGuard] ,
  children: [
      { path: 'customer-configurations', component: CustomersettingsComponent,canActivate: [AdminGuard] },
      { path: 'user-configurations', component: UsersettingsComponent ,canActivate: [AdminGuard] },

    ],
},
]

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    UserSettingsModule,
    RouterModule.forChild(routes),
  ]
})
export class ConfigurationsModule { }
