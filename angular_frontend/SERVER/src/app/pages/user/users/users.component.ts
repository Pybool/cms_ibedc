import { Observable } from 'rxjs';
import { FetchUsers, LoadUser } from './state/user.actions';
import { UserService } from 'src/app/services/user.service';
import { Component, ComponentFactoryResolver, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { userdata } from './usersdata'
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { usersData } from './state/user.selector';
import { UserFilters, UserModifyModel } from '../createuser/models/user';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  public dev_perm:boolean = true;
  public usersData = userdata;
  userListState:Observable<any>;
  usersListObs$:any;
  filter = new UserFilters()
  @ViewChild('edituserplaceholder', { read: ViewContainerRef }) placeholder: ViewContainerRef;

  constructor(private store: Store<AppState>,
    private userService:UserService,
    private componentFactoryResolver: ComponentFactoryResolver) {
    this.store.dispatch(new FetchUsers());
   }

  ngOnInit(): void {
    this.userListState = this.store.select(usersData);
    this.userService.fetchusers().subscribe((users) => {
      this.usersData = users.data.users
      this.userService.storePositions(users.data.user_positions)
      
    })
  }

  viewMode(){

  }

  
  editUserForm(){
    import('./../edituser/edituser.component').then(({ EdituserComponent }) => {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(EdituserComponent);
      const editComponent:any = this.placeholder?.createComponent(componentFactory);
      this.userService.cacheEditComponent(editComponent)
      document.getElementById('edit_user')?.classList.add("content-active")
    });
    

  }
  createUserForm(){
    import('./../createuser/createuser.component').then(({ CreateuserComponent }) => {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(CreateuserComponent);
      this.placeholder?.createComponent(componentFactory);
      document.getElementById('create_user')?.classList.add("content-active")
    });
    
  }

  getItemById(array, id) {
    return array.find(item => item.id === id);
  }

  formatUser(user):any{
    return (
        user.name,
        user.email,
        user.password,
        user.position,
        user.permission_hierarchy,
        user.can_create_customer,
        user.can_approve,
        user.can_approve_caad,
        user.can_manage_2fa,
        user.hq_radio,
        user.region_radio,
        user.bizhub_radio,
        user.service_center_radio,
        user.permissions_hierarchy,
        user.groups,
        user.enable_2fa,
        user.region,
        user.business_unit,
        user.servicecenter
      )

  }

  getSingleUser(id){
    this.userService.getSingleUser(id,this.usersData)
    this.editUserForm()
  }

  submitFilter(){
    console.log(this.filter)
  }

  getResetUser2FA(id){

  }

  getSuspendUser(self){

  }

  resetFilter(){
    this.filter = new UserFilters()
  }

  

}
