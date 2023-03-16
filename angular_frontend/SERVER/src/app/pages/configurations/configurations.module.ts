import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfigurationsComponent } from './configurations.component';
import { RouterModule, Routes } from '@angular/router';
import { CustomersettingsComponent } from './customersettings/customersettings.component';
import { UsersettingsComponent } from './usersettings/usersettings.component';
import { UserSettingsModule } from './usersettings/usersettings.module';

const routes: Routes = [{
  path: '',
  component: ConfigurationsComponent,
  children: [
      { path: 'customer-configurations', component: CustomersettingsComponent },
      { path: 'user-configurations', component: UsersettingsComponent },

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
