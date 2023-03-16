import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CreateuserComponent } from './createuser.component';
import { SharedModule } from '../shared.module';


@NgModule({
  declarations: [
    CreateuserComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule
    
  ],
  exports: [
    CreateuserComponent
  ]
})
export class CreateuserModule { }

// error NG6007: The Component 'CustomselectComponent' is declared by more than one NgModule.
