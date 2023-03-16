import { Component } from '@angular/core';
import * as helper from '../scripts'

@Component({
  selector: 'app-customersettings',
  templateUrl: './customersettings.component.html',
  styleUrls: ['./customersettings.component.css']
})
export class CustomersettingsComponent {

  constructor(){}

  ngOninit(){

  }

  handleCustomize($event){
    console.log("====> ",$event.target.value)
    helper.handleCustomize($event.target.value)

  }


}
