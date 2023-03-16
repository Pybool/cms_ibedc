import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CustomselectComponent } from 'src/app/ui/customselect/customselect.component';

@NgModule({
  declarations: [
    CustomselectComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
  ],
  exports: [
    CustomselectComponent
  ]
})
export class SharedModule { }