import { UserService } from 'src/app/services/user.service';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { AppState } from 'src/app/basestore/app.states';
import { Store } from '@ngrx/store';
import { usersData } from '../users/state/user.selector';
import { UpdateUser } from '../createuser/models/user';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { UserState } from 'src/app/authentication/state/auth.selector';
import { getLocationsState } from 'src/app/ui/customselect/state/customselect.selector';
import { UpdateExistingUser } from '../state/createuser.actions';

const  _ = require('lodash');

@Component({
  selector: 'app-edituser',
  templateUrl: './edituser.component.html',
  styleUrls: ['./edituser.component.css']
})
export class EdituserComponent implements OnInit {
  userForm!: FormGroup;
  id;
  user: any = new UpdateUser();
  positions = []
  userListState:any;
  usersListObs$:any;
  permission_hierarchy:any;
  options:any[];
  groups:any[];
  regions = []
  bizhubs = []
  servicecenters = []
  userState;
  can_create_user;
  getLocations;
  title;
  // @Input() selectedOption: any;
  @Output() selectionChange = new EventEmitter<any>();
  @Output() type = new EventEmitter<any>();
  @Output() updatetitle = new EventEmitter<any>();
  
  constructor(private store: Store<AppState>,private userService: UserService) { 
    this.userState = this.store.select(UserState);
    this.getLocations = this.store.select(getLocationsState);
    
    console.log(this.user)
    this.userListState = this.store.select(usersData);
    this.usersListObs$ = this.userListState.subscribe((user) => {
      if(user.isFetched){
        this.positions = user.users.user_positions
      }
      else{
        this.positions = []
      }
    });
    this.userService.fetchMetadata().subscribe((data) => {
      this.options = data.positions
      this.groups = data.groups
      for (let obj of data.regions){
        this.regions.push(obj.region)
      }
    });

    this.userState.subscribe((user) => {
      if (user == undefined){
      }
      else{
        this.can_create_user = user.can_create_user
      }
    });

  }

  ngOnInit(): void {
    console.log("-------------------------------------------->")
    this.userForm = new FormGroup({
      name: new FormControl(null, Validators.required),
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, Validators.required),
      position: new FormControl(null),
      privilege: new FormControl(null),
      can_create_customers: new FormControl(false),
      can_create_user: new FormControl(false),
      can_approve: new FormControl(false),
      can_approve_caad: new FormControl(false),
      can_manage_2fa: new FormControl(false),
      permission_hierarchy: new FormControl(false),
      groups: new FormControl(null),
      enable_2fa: new FormControl(false),
      region: new FormControl(null),
      business_unit: new FormControl(null),
      servicecenter: new FormControl(null),
    });
  
    this.userService.returnUser().subscribe((data) => {
      this.user = data.user
      this.id = data.id
      
      this.userForm.patchValue(this.user);
      this.userForm.patchValue({permission_hierarchy:this.user.permissions_hierarchy})
      console.log("Patch ===> ", this.user, this.userForm)
      this.title = this.user.position
      
      let radioIds = {'Head Quarters':'hq_radio__update','Region':'region_radio__update','Business Hub':'bizhub_radio__update','Service Center':'service_center_radio__update'}
      let radio:any = document.getElementById(radioIds[this.user.permissions_hierarchy])
      this.permission_hierarchy = this.user.permissions_hierarchy
      
      radio.checked = true;
      console.log(this.permission_hierarchy)

      
    })
    
  }

  getPositionVal(position){


    const positionList = document.querySelector("#app-user-positions-update").querySelector('ul');
    const searchText = position;
    const liElements = positionList.querySelectorAll("li");
    
    for (let i = 0; i < liElements.length; i++) {
      if (liElements[i].textContent.includes(searchText)) {
        // The text was found in this li element, so return it
        return liElements[i].querySelector('a').name;
      }
    }
    
    // The text was not found in any of the li elements
    return null;
    
    
    }

  ngAfterViewInit(){
    let dropdown = document.getElementById('app-user-positions-update')
      if(dropdown != null){
        console.log(dropdown.querySelector('a'),this.user.position)
        dropdown.querySelector('a').setAttribute('name',this.getPositionVal(this.user.position))
      }
      else{}

    let regiondropdown = document.getElementById('app-regions-update')
      if(regiondropdown != null){
        console.log(regiondropdown.querySelector('a'),this.user.region)
        regiondropdown.querySelector('a').setAttribute('name',this.user.region)
      }
      else{}

    this.userService.fetchUserGroups().subscribe((data) => {
      console.log(data)
      let selectElement:any = document.getElementById("groups");
      // Select the first and third options
      let selectedValues = data.data.map(function(item) {
        return item.id;
      });
      selectElement.value = selectedValues;
    this.userForm.patchValue({groups:selectedValues})
      for(let group of data.data){
        let index = this.findOptionIndex(selectElement,group.name)
        console.log(index)
        if(index != -1){
          selectElement.options[index].selected = true;
        }
        else{console.log("Not found")}
        
      }
      

    })

      
  }

  findOptionIndex(selectId, targetText) {
  
    var options = selectId.options;
  
    for (var i = 0; i < options.length; i++) {
      if (options[i].text.includes(targetText)) {
        return i;
      }
    }
  
    // Return -1 if no option is found
    return -1;
  }
  

  radioPermissionsSelector(e,val){
    let id = e.target.id
    let radio:any = document.getElementById(id)
    radio.checked = true;
    this.permission_hierarchy = val
    this.user.permission_hierarchy = val
    this.userForm.patchValue({permission_hierarchy:this.permission_hierarchy})
}

getDropdownsValues(){
  let ids = {'region':'app-regions-update','position':'app-user-positions-update',
            'privilege':'app-can-create-users','business_unit':'app-bizhubs-update',
            'servicecenter':'app-servicecenters-update'
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
          let patch = { [`${key}`]: String(value)?.trim() }
          if (id ==  'app-user-positions-update'){
            console.log("Patch positions ===> ",dropdown, id ,value)
            console.log(patch)
          }
          this.userForm.patchValue(patch)
        }
        else{this.userForm[key] = ""}
      }
    }
  
}
}

updateBizHubs($event,id){
  if ($event.length > 0){
    this.bizhubs = $event
  }
  
}

patchForm($event,type){
  this.userForm.patchValue({region:$event});
  if(type=='region'){
    this.user.region = $event
  }
  else if(type=='bizhub'){
    this.user.business_unit = $event
  }
  else if(type=='servicecenter'){
    this.user.servicecenter = $event
  }
  
  console.log(this.user)
  // alert($event)
}

updateServiceCenters($event,id){
  if ($event.length > 0){
    this.servicecenters = []
    this.servicecenters = $event
    console.log("#########Service centers Events ====> ", this.servicecenters)
  }
}
    
  submit(){
    this.getDropdownsValues()
    let payload = this.userForm.value
    payload['id'] = this.id
    console.log(payload)
    this.store.dispatch(new UpdateExistingUser(payload));
    // this.userForm = Object.assign({}, this.userForm);
  }
  

  exitForm(){
    this.userForm = new FormGroup({
      name: new FormControl(null, Validators.required),
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, Validators.required),
      position: new FormControl(null),
      privilege: new FormControl(null),
      can_create_customers: new FormControl(false),
      can_create_user: new FormControl(false),
      can_approve: new FormControl(false),
      can_approve_caad: new FormControl(true),
      can_manage_2fa: new FormControl(false),
      permission_hierarchy: new FormControl(false),
      groups: new FormControl(null),
      enable_2fa: new FormControl(false),
      region: new FormControl(null),
      business_unit: new FormControl(null),
      servicecenter: new FormControl(null),
    });
    document.getElementById('edit_user').classList.remove("content-active")
    console.log(document.getElementById('edit_user').classList)
    document.getElementById('edit_user').classList.remove("content-active") 
}

}
