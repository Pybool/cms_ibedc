import { Component ,OnInit} from '@angular/core';
import {Router} from '@angular/router'; // import router from angular router
import { Store } from '@ngrx/store';
import { AppState } from './basestore/app.states';
import {  getStoredState } from './basestore/app.reducer';
import { initialState } from './authentication/state/auth.reducer';
import { RehydrateLogIn } from './authentication/state/auth.actions';
import { isAuthenticated, UserState } from './authentication/state/auth.selector';
import { AuthService } from './services/auth.service';
import { User } from './authentication/models/user';
import { ActivatedRoute } from '@angular/router';
import { SharedService } from './services/shared.service';
import { CustomerService } from './services/customer.service';
import { DeepFetchEcmiCustomers, DeepFetchEmsCustomers } from './pages/customers/state/customer.actions';

declare function myfunction(): any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'cms-ibedc-app';
  usersMail= ''
  usersName = ''
  getState;
  userState;
  auth_user:User;
  can_approve:boolean;
  can_approve_caad:boolean;
  is_authenticated:boolean;
  activeInput:string;
  activeCustomerPage:string;
  
  constructor(private router: Router,
              private store: Store<AppState>,
              private authService: AuthService,
              private route: ActivatedRoute,
              private sharedService:SharedService,
              private customerService:CustomerService) {
    this.store.dispatch(new RehydrateLogIn(''));
    this.getState = this.store.select(isAuthenticated);
    this.userState = this.store.select(UserState);
  }

 
  ngOnInit(){

    this.sharedService.getActiveSearchInput()?.subscribe({
      next: activeInput => {
        this.activeInput = activeInput
      },
    });

    this.sharedService.getActiveCustomerPage()?.subscribe({
      next: activePage => {
        this.activeCustomerPage = activePage
      },
    });
    
    this.getState.subscribe((state) => {
      this.is_authenticated = true
    });

    this.userState.subscribe((user) => {
      console.log(user)
      if (user == undefined){
        this.router.navigateByUrl("/cms/web/login")
      }
      else{

        this.can_approve = user.can_approve
        this.can_approve_caad = user.can_approve_caad
        // this.router.navigateByUrl("/dashboard")
      }
    });

    (function(){
      const dropdowns = document.querySelectorAll('.dropdown');
      const dropups = document.querySelectorAll('.dropup');
      dropdowns.forEach(dropdown => {
          dropdown.addEventListener('mouseover', function hoverOn(event) {
              try{dropdown.children[1].classList.add('show');}
              catch{}
          });
          dropdown.addEventListener('mouseout', async function hoverOut(event) {
              try{dropdown.children[1].classList.remove('show');}
              catch{}
          });
      });
      
      dropups.forEach(dropup => {
          dropup.addEventListener('mouseover', function hoverOn(event) {
              dropup.children[1].classList.add('show');
          });
          dropup.addEventListener('mouseout', async function hoverOut(event) {
              
              dropup.children[1].classList.remove('show');
          });
      });
    })()
    
  }

  darkMode(){

  }

  searchCustomer($event){
    console.log('xxx',$event.target.value)
    this.sharedService.searchCustomer($event)
  }

  abbreviateName(usersName){

  }

  changeSearchTable($event){
    
    console.log($event.target.checked)
    let inputEl:any = document.querySelector('#search-customer-input')
    if ($event.target.checked){
      inputEl.placeholder = `Search for a ${this.activeCustomerPage} customer`
    }
    else{inputEl.placeholder = `Search for a customer`}
  }

  searchBarFilter($event){
    var searchBar:any = document.querySelector('#search-customer-input')
    if(searchBar){
      let searchBarValue = searchBar.value.trim();
      console.log(searchBarValue)
      if (searchBarValue.trim().length > 0){
          //Dispatch deepSearch service here
          let payload = {activePage:this.activeCustomerPage,fieldName:$event.target.name,q:[searchBarValue]}
          if(this.activeCustomerPage == 'prepaid'){
            this.store.dispatch(new DeepFetchEcmiCustomers(payload))
            // this.customerService.deepFetchCustomers(this.activeCustomerPage,$event.target.name,searchBarValue)
          }
          else if(this.activeCustomerPage == 'postpaid'){
            this.store.dispatch(new DeepFetchEmsCustomers(payload))
            // this.customerService.deepFetchCustomers(this.activeCustomerPage,$event.target.name,searchBarValue)
          }
          
          console.log(`Searching for a ${$event.target.textContent} ==> `, searchBarValue)
      }
      else{
        console.log("Search Bar Empty!",`Please type a/an ${$event.target.textContent}  in the search bar and click ${$event.target.textContent} filter again`)
      }
    }
    else{alert("Component is not loaded yet.")}
    
  }

  
  logout(){
    
    this.authService.logout()
    this.is_authenticated = false;
  }

ngAfterViewInit() {
  
  try{
    myfunction()
    
  }
  catch(err:any){
    
  }
  
  
}

}
