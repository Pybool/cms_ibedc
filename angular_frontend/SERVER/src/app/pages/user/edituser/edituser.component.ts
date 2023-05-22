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
import { CustomerService } from 'src/app/services/customer.service';
import { NotificationService } from 'src/app/services/notification.service';
import { take } from 'rxjs/operators';

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
  regions = [];
  business_units = []
  service_centers = []
  userState;
  can_create_user;
  getLocations;
  title;
  value
  // @Input() selectedOption: any;
  @Output() selectionChange = new EventEmitter<any>();
  @Output() type = new EventEmitter<any>();
  @Output() updatetitle = new EventEmitter<any>();
  
  constructor(private store: Store<AppState>,
    private userService: UserService,
    private customerService: CustomerService,
    private notificationService: NotificationService) { 
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
      groups: new FormControl(undefined),
      enable_2fa: new FormControl(false),
      region: new FormControl(null),
      business_unit: new FormControl(null),
      servicecenter: new FormControl(null),
    });
  
    this.userService.returnUser().subscribe((data) => {
      this.user = data.user
      this.id = data.id
      this.userService.fetchUserLocationMetadata({region:this.user.region,business_unit:this.user.business_unit,serviccenter:this.user.servicecenter})
      .subscribe((data:any) => {
          this.regions = data.regions
          this.business_units = data.business_units
          this.service_centers = data.servicecenters
          this.groups = data.groups
          this.userForm.patchValue({business_unit:this.user.business_unit})
          this.userForm.patchValue({servicecenter:this.user.servicecenter})
          console.log(this.user)
          
        });
      
      this.userForm.patchValue(this.user);
      this.userForm.patchValue({permission_hierarchy:this.user.permissions_hierarchy})
      this.userForm.patchValue({region:this.user.region})
      console.log("Patch ===> ", this.user, this.userForm)
      this.title = this.user.position
      
      let radioIds = {'Head Quarters':'hq_radio__update','Region':'region_radio__update','Business Unit':'bizhub_radio__update','Service Center':'service_center_radio__update'}
      let radio:any = document.getElementById(radioIds[this.user.permissions_hierarchy])
      this.permission_hierarchy = this.user.permissions_hierarchy
      radio.checked = true;
      
    })
    
  }

  toTitleCase(str) {
    return str.replace(
      /\w\S*/g,
      function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      }
    );
  }

  getPositionVal(position){
    let positionDropdown:any = document.querySelector("#position-dropdown-menu")
    let positionList = positionDropdown.querySelectorAll('ul');
    const searchText = position;
    if(positionList.length > 0){
      const liElements = positionList[0].querySelectorAll("li");
      for (let i = 0; i < liElements.length; i++) {
        if (liElements[i]?.textContent.includes(searchText)) {
          return liElements[i]?.querySelector('a')?.name;
        }
      }
    }
    
    return null;
    }

  ngAfterViewInit(){

    let regiondropdown = document.getElementById('app-regions-update')
      if(regiondropdown != null){
        console.log(regiondropdown.querySelector('a'),this.user.region)
        regiondropdown.querySelector('a').setAttribute('name',this.user.region)
      }
      else{}

    this.userService.fetchUserGroups().subscribe((data) => {
      let selectElement:any = document.getElementById("groups");
      let selectedValues = data.data.map(function(item) {
        return item.id;
      });
      selectElement.value = selectedValues;
    this.userForm.patchValue({groups:selectedValues})
      for(let group of data.data){
        let index = this.findOptionIndex(selectElement,group.name)
        console.log(selectedValues)
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

  onSelect($event){
    let dropdown:any = document.getElementById('position-dropdown')
      if(dropdown != null){
        console.log(dropdown,this.user.position,$event.target.textContent)
        // this.value = this.getPositionVal(this.user.position)
        console.log(this.positions, $event.target.value)
        dropdown.name =  $event.target.closest('a').name
        dropdown.innerHTML = $event.target.textContent
      }
      else{}

  }
  

  radioPermissionsSelector(e,val){
    let id = e.target.id
    let radio:any = document.getElementById(id)
    radio.checked = true;
    this.permission_hierarchy = val
    this.user.permission_hierarchy = val
    this.userForm.patchValue({permission_hierarchy:this.permission_hierarchy})
}

getPositionCodeObj(array, name) {
  return array.find(item => item.name === name);
}

getDropdownsValues(){
  let ids = {'position':'position-dropdown-menu'}
            
  for(let key of Object.keys(ids)){
    let id = ids[key]
    let dropdown:any = document.getElementById(id)
    if(dropdown != null){
      if (Array.from(dropdown.querySelector('ul.link-list-opt').children).length< 1){
        return 
      }
      else{
        dropdown = document.getElementById('position-dropdown')
        let value = dropdown?.name;
        if (value != undefined && value != null){
          
          let patch = { [`${key}`]: String(value)?.trim() }
          if (id ==  'position-dropdown-menu'){
            if(key=='position' && value==''){
              
              this.userService.getPositions().pipe(take(1)).subscribe((positions)=>{
                const positionObj = this.getPositionCodeObj(positions,this.user.position)
                this.user.position = positionObj?.code
                patch = { [`${key}`]: this.user.position }
              })
            }
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
    // this.bizhubs = $event
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
    this.service_centers = []
    this.service_centers = $event
    console.log("#########Service centers Events ====> ", this.service_centers)
  }
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

    
  submit(){
    this.getDropdownsValues()
    let payload = this.userForm.value
    payload['id'] = this.id
    console.log(payload)
    this.store.dispatch(new UpdateExistingUser(payload));
    // this.userForm = Object.assign({}, this.userForm);
  }
  

  exitForm(){
    this.userService.destoryEditComponent()
    document.getElementById('edit_user').classList.remove("content-active")
}

}
