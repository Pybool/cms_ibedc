import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { UsersettingsComponent } from './usersettings.component';

const routes: Routes = []

@NgModule({
  declarations: [UsersettingsComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ]
})
export class UserSettingsModule { }
