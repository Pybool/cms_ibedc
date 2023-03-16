import { UserService } from 'src/app/services/user.service';
import { CreateNewUser } from '../state/createuser.actions';
import { CreateUser } from './models/user';
import { Component, EventEmitter, Input, OnInit, Output, OnDestroy } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { UserState } from 'src/app/authentication/state/auth.selector';
import { getLocationsState } from 'src/app/ui/customselect/state/customselect.selector';
import { CustomerService } from 'src/app/services/customer.service';
// const  _ = require('lodash');

@Component({
  selector: 'app-createuser',
  templateUrl: './createuser.component.html',
  styleUrls: ['./createuser.component.css']
})
export class CreateuserComponent implements OnInit {

  form!: FormGroup;
  user: CreateUser = new CreateUser();
  getState: Observable<any>;
  errorMessage: string | null;
  newUserpayload:any;
  metaData$:Observable<any>;
  options:any[];
  groups:any[];
  priviledges:any[] = [{name:'Can Create Users',code:'Can Create Users'},{name:'Cannot Create Users',code:'Cannot Create Users'}]
  userState;
  permission_hierarchy:any;
  can_create_user = true;
  regions = []
  business_units = []
  service_centers = []
  // @Input() selectedOption: any;
  @Output() selectionChange = new EventEmitter<any>();
  @Output() type = new EventEmitter<any>();
  getLocations;
  locations$: any;
  
  constructor(
    private store: Store<AppState>,private userService:UserService, private customerService:CustomerService
  ) {
    this.userState = this.store.select(UserState);
    this.getLocations = this.store.select(getLocationsState);
  }

  ngOnInit(): void {
   
   this.userService.fetchMetadata().subscribe((data) => {
      this.options = data.positions
      this.groups = data.groups
      console.log(data.regions)
      this.regions = data.regions
    });

    this.userState.subscribe((user) => {
      if (user == undefined){
      }
      else{
        this.can_create_user = user.can_create_user
      }
    });
  }

  getDropdownsValues(){
    let ids = {'region':'app-regions','position':'app-user-positions',
              'privilege':'app-can-create-users','business_unit':'app-bizhubs',
              'servicecenter':'app-servicecenters'
            }
              
    for(let key of Object.keys(ids)){
      let id = ids[key]
      let dropdown = document.getElementById(id)
      if(dropdown != null){
        if (Array.from(dropdown.querySelector('ul.link-list-opt').children).length< 1){
          return 
        }
        else{
          let value = dropdown.querySelector('a')?.name;
          if (value != undefined && value != null){
            this.user[key] = String(value)?.trim()
          }
          else{this.user[key] = ""}
        }
      }
    
  }
}

  submit() {
    
    this.newUserpayload = {email:this.user.email,password:this.user.password}
    this.getDropdownsValues()
    this.store.dispatch(new CreateNewUser(this.user));
    this.user = Object.assign({}, this.user);
  }

  radioPermissionsSelector(e,val){
      let id = e.target.id
      let radio:any = document.getElementById(id)
      radio.checked = true;
      this.permission_hierarchy = val
      this.user.permission_hierarchy = val
  }

  fetchServiceCenters($event){
    this.customerService.fetchLocations('servicecenter',$event.target.value).subscribe((data)=>{
      this.service_centers = data.data.service_centers
    })
  }

  fetchBusinessUnits($event){
    this.customerService.fetchLocations('business_unit',$event.target.value).subscribe((data)=>{
      this.business_units = data.data.business_units
      this.service_centers = []
    })
  }

  exitForm(){
    document.getElementById('create_user').classList.remove("content-active")
    console.log(document.getElementById('create_user').classList)
    document.getElementById('create_user').classList.remove("content-active")
  }

  ngOnDestroy(){

  }


}
