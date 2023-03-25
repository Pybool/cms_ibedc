import { Component ,OnInit} from '@angular/core';
import {Router} from '@angular/router'; // import router from angular router
import { Store } from '@ngrx/store';
import { AppState } from './basestore/app.states';
import {  getStoredState } from './basestore/app.reducer';
import { initialState } from './authentication/state/auth.reducer';
import { abbreviateName } from './../utils'
import { RehydrateLogIn } from './authentication/state/auth.actions';
import { isAuthenticated, UserState } from './authentication/state/auth.selector';
import { AuthService } from './services/auth.service';
import { User } from './authentication/models/user';
import { ActivatedRoute } from '@angular/router';
import { SharedService } from './services/shared.service';
import { CustomerService } from './services/customer.service';
import { DeepFetchEcmiCustomers } from './pages/customersmodule/prepaidcustomers/state/customer.actions';
import { DeepFetchEmsCustomers } from './pages/customersmodule/postpaidcustomers/state/customer.actions';
import { SpinnerService } from './services/spinner.service';
import { BillingService } from './services/billing.service';
import { take } from 'rxjs/operators';
import { NotificationService } from './services/notification.service';

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
  abbreviateName = abbreviateName
  getState;
  userState;
  auth_user:User;
  can_approve:boolean;
  can_approve_caad:boolean;
  is_authenticated:boolean;
  activeCustomerPage:string;
  activeSearchbar:string = 'customers'
  
  constructor(private router: Router,
              private store: Store<AppState>,
              private authService: AuthService,
              private route: ActivatedRoute,
              private sharedService:SharedService,
              private customerService:CustomerService,
              private spinnerService:SpinnerService,
              private billingService:BillingService,
              private notificationService:NotificationService) {
    this.store.dispatch(new RehydrateLogIn(''));
    this.getState = this.store.select(isAuthenticated);
    this.userState = this.store.select(UserState);
  }

 
  ngOnInit(){

    this.sharedService.getActiveSearchInput()?.subscribe({
      next: activeSearchbar => {
        this.activeSearchbar = activeSearchbar
      },
    });


    this.sharedService.getActiveCustomerPage()?.subscribe({
      next: activePage => {
        this.activeCustomerPage = activePage
      },
    });
    
    this.getState.subscribe((state) => {
      // this.is_authenticated = true //HOW THE FUCK ???????????
    });

    this.userState.subscribe((user) => {
      console.log(user)
      if (user == undefined){
        this.router.navigateByUrl("/cms/web/login")
      }
      else{

        this.can_approve = user.can_approve
        this.can_approve_caad = user.can_approve_caad
        this.usersMail = user.email
        this.usersName = user.name
        this.is_authenticated = true
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
    this.sharedService.searchCustomer($event)
  }

  shallowSearchBilling($event){
    this.sharedService.shallowSearchBilling($event)
  }
  

  activateDualSearch($event){
    this.sharedService.activateDualSearch($event.target.checked)
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
            const parentElement = document.getElementById('search-status');
            this.spinnerService.showSpinner(parentElement);
            this.sharedService.setSpinnerText('Processing your request')
            this.store.dispatch(new DeepFetchEcmiCustomers(payload))
          }
          else if(this.activeCustomerPage == 'postpaid'){
            const parentElement = document.getElementById('ems-search-status');
            this.spinnerService.showSpinner(parentElement);
            this.sharedService.setSpinnerText('Processing your request')
            this.store.dispatch(new DeepFetchEmsCustomers(payload))
          }
          
          console.log(`Searching for a ${$event.target.textContent} ==> `, searchBarValue)
      }
      else{
        console.log("Search Bar Empty!",`Please type a/an ${$event.target.textContent}  in the search bar and click ${$event.target.textContent} filter again`)
      }
    }
    else{alert("Component is not loaded yet.")}
    
  }

  billingSearchBarFilter($event){
    var searchBar:HTMLInputElement = document.querySelector('#billing-history-search-bar')
    if(searchBar){
      let searchBarValue = searchBar.value.trim();
      console.log(searchBarValue)
      if (searchBarValue.trim().length > 0){
          //Dispatch deepSearch service here
          let payload = {type:'searchbar',activePage:'billing',fieldName:$event.target.name,q:[searchBarValue.trim()]}
            const parentElement = document.getElementById('spinner-wrapper');
            this.spinnerService.showSpinner(parentElement);
            this.sharedService.setSpinnerText('Processing your request')
            console.log("Billing search payload ====> ", payload)
            this.billingService.deepSearchBilling(payload).pipe(take(1)).subscribe((response)=>{
              if (response.status){
              //Load toastr Notification Modal here...
              this.billingService.swapBillinglist(response)
                this.notificationService.success('Records matching your search criteria were found','Search results found',{})
              }
              else{
                //Load Notification Modal here....
                let notification = {type:'failure',title:'Oops!!!',
                message:'Could not retrieve results for your search criteria at this time',
                subMessage:'Something isn\'t right '}
                this.notificationService.setModalNotification(notification)
              }
            },
            error=>{
                //Load Notification Modal here....
                let notification = {type:'failure',title:'Oops!!!',
                message:'Could not retrieve results for your search criteria at this time',
                subMessage:'An error occured somewhere...'}
                this.notificationService.setModalNotification(notification)

              }
            )          
          console.log(`Searching for a ${$event.target.textContent} ==> `, searchBarValue)
      }
      else{
        let notification = {type:'failure',title:'???',
        message:(`Please type a/an ${$event.target.textContent}  in the search bar and click ${$event.target.textContent} filter again`),
        subMessage:'No search criterion'}
        this.notificationService.setModalNotification(notification)
        console.log()
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
