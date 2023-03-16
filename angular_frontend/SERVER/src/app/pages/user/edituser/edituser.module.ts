import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { EdituserComponent } from './edituser.component';
import { SharedModule } from '../shared.module';



@NgModule({
  declarations: [
    EdituserComponent,
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
    EdituserComponent
  ]
})
export class EdituserModule { }
