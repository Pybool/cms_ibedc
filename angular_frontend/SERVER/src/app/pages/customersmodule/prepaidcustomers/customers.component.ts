import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnInit,AfterViewInit, Renderer2, ViewChild, ViewContainerRef } from '@angular/core';
import { customerData } from './customerdata.js'
import { abbreviateName } from '../../../../utils'
import { of } from 'rxjs';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';
import { AppState } from 'src/app/basestore/app.states';
import { Store } from '@ngrx/store';
import { isAuthenticated, UserState } from 'src/app/authentication/state/auth.selector';
import { FetchEcmiCustomers, FetchEmsCustomers } from './state/customer.actions';
import { ecmiCustomers, emsCustomers } from './state/customer.selector';
import { SharedService } from 'src/app/services/shared.service';
import { CustomerFilter } from './models/customer';
import { CustomerService } from 'src/app/services/customer.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgZone } from '@angular/core';
import { map, take, tap } from 'rxjs/operators';
import { DataTablesModule } from 'angular-datatables';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { DataTableDirective } from 'angular-datatables';
import { SpinnerService } from 'src/app/services/spinner.service';
import { ConvertTableService } from 'src/app/services/convert-table.service';

interface CustomWindow extends Window {
  waitForElm:(arg1) => any;
  DataTable: (searchTerm: string,{}) => void;
}

declare let window: CustomWindow;

// Helper function to set dropdown value

// import { DataTable } from "./datatables.js"
@AutoUnsubscribe
@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.css']
})
export class CustomersComponent implements AfterViewInit {
  public metaData;
  dtOptions: DataTables.Settings = {};
  @ViewChild(DataTableDirective)
  datatableElement: DataTableDirective;
  filter:any = new CustomerFilter()
  create_perm:boolean;
  can_approve:boolean;
  has_field:boolean;
  appname:string;
  advanced_filters:boolean ;
  transients;
  defaults;
  field_names;
  current_user;
  Math = Math
  abbreviateName = abbreviateName
  custs$;
  customers$:any;
  deferredItems = [];
  getState;
  userState;
  can_approve_caad:boolean;
  can_create_customers:boolean;
  ecmiCustomersList
  emsCustomersList
  activePage = ''
  customersType:string;
  isAuthenticated:boolean = false;
  ems_total_customers = 0
  ecmi_total_customers = 0
  emsCustomersList$;
  ecmiCustomersList$;
  regions = null;
  business_units:any[] = []
  service_centers:any[];
  mode;
  currentAccountno;
  ecmi_total_customers$
  ems_total_customers$
  intervalId
  isCallable:boolean = true
  // dtOptions: DataTables.Settings = {};
  @ViewChild('editcustomerplaceholder', { read: ViewContainerRef }) placeholder: ViewContainerRef;
  @ViewChild('createcustomerplaceholder', { read: ViewContainerRef }) createplaceholder: ViewContainerRef;
  constructor(private store: Store<AppState>,
              private zone: NgZone,
              private sharedService:SharedService,
              private cd: ChangeDetectorRef,
              private customerService:CustomerService,
              private componentFactoryResolver: ComponentFactoryResolver,
              private renderer: Renderer2,
              private spinnerService: SpinnerService,
              private convertTableService:ConvertTableService,
              private route: ActivatedRoute,) { 
    this.sharedService.setActiveSearchInput('customers')
    this.custs$ = customerData.customer_data
    this.metaData = customerData.metadata
    this.can_create_customers = false;
    this.can_approve= this.metaData.can_approve;
    this.has_field= this.metaData.has_field;
    this.appname = this.metaData.appname;
    this.advanced_filters= this.metaData.advanced_filters;
    this.transients = customerData.transients;
    this.defaults = customerData.defaults;
    this.field_names = customerData.field_names;
    this.current_user = customerData.current_user;
    this.Math = Math
    this.abbreviateName = abbreviateName;
    this.getState = this.store.select(isAuthenticated);
    this.userState = this.store.select(UserState);
    this.ecmiCustomersList = this.store.select(ecmiCustomers);
    //Dispatch a request for Prepaid Customers by default....
    this.zone.runOutsideAngular(() => {
      this.store.dispatch(new FetchEcmiCustomers());
      this.zone.run(() => {
        
      });
    });
  }

  ngOnInit(): void {
    //Check if user is authenticated
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
    this.dtOptions = {
      responsive: true
    };
    
    this.getState = this.store.select(isAuthenticated);
    this.getState.subscribe((state) => {
      this.isAuthenticated = state
    });

    /* For swapping customer list observable after searching for customers with neither search bar or advanced filters */
    this.customerService.getNewCustomerList().subscribe((data)=>{
      console.log(data)
      this.sharedService.setSpinnerText('Processing search results..')
      this.ecmi_total_customers = data?.total_customers
      this.customers$ = of(data.data)
      this.spinnerService.hideSpinner()
      setTimeout(()=>{//Wait for table to render search results and dispatch keydown to show table rows
        const searchBar:HTMLInputElement = document.querySelector('#search-customer-input')
        const keyEvent = new KeyboardEvent('keyup', { key: 'Enter' });
        searchBar.dispatchEvent(keyEvent);
      },500)
      
    })
    
    this.userState.subscribe((user) => {
       this.can_create_customers = user.can_create_customer
    });

      this.ecmiCustomersList$ = this.ecmiCustomersList.subscribe((data:any) => {
        this.sharedService.setActiveCustomerPage('prepaid')
        this.customersType = 'prepaid'
        this.activePage = 'prepaid'
        this.customers$ = of(data.customers)//user.can_create_customers
        this.ecmi_total_customers = data.total_customers
        console.log("=====> Done setting ECMI customers ",this.ecmi_total_customers)
        this.sharedService.setSpinnerText('Processing data...')
      
      })
    }

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);
  }
 
  loadCustomerInformation($event,accountno,meterno,accounttype){
    let base = `customer/information/basic-information`
    const queryParams = {accountno : accountno, accounttype: accounttype?.toLowerCase(),meterno:meterno };
    this.sharedService.navigateWithParams(base,queryParams)
  }

  openCustomerCreateForm(){
    this.createCustomerForm().then((status)=>{
      console.log(document.getElementById('create_customer').classList)
      document.getElementById('create_customer').classList.add("content-active")
      
    })
    this.sharedService.setFormHeader(['Create Awaiting Customer'])
    this.mode = 'create'
    
  }

  openDrafts(){
    this.createCustomerForm().then((status)=>{
      document.getElementById('create_customer').classList.add("content-active")
      document.getElementById('creation-draft').click()
    
    })
  }

  openCustomerUpdateForm($event){
    console.log($event.target)
    this.currentAccountno = $event.target.closest('a').id
    console.log("Account no ===> ", this.currentAccountno)
    this.openCustomerCreateForm()//Bug
    this.sharedService.setFormHeader(['edit','Update Existing Customer',this.activePage,this.currentAccountno])
    this.mode = 'edit'
  }

  getRandomColor() {
    if(this.isCallable){
      return Math.floor(Math.random() * 16777215).toString(16);
    }
    
  }

  ngAfterViewInit(){
    const parentElement = document.getElementById('table-wrapper');
    console.log("---------> ", parentElement)
    this.spinnerService.showSpinner(parentElement);
    this.sharedService.setSpinnerText('Fetching data from source...')
    this.convertTableService.convertTable({id:'customer_table'}).then((status)=>{
      if(status){
        this.isCallable = false
      }
    })
    
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

  submitFilter(){
    Object.keys(this.filter).forEach((key)=>{
      if (this.filter[key] == '' || this.filter[key]==undefined || this.filter[key] == null){
        Reflect.deleteProperty(this.filter, key);
      }
    })
    const parentElement = document.getElementById('search-status');
    console.log("---------> ", parentElement)
    this.spinnerService.showSpinner(parentElement);
    this.sharedService.setSpinnerText('Processing your request')
    this.customerService.advancedFilterEcmiCustomers(this.filter).pipe(take(1)).subscribe((response)=>{
       this.customerService.swapCustomerlist(response)
    })
  }

  getRegions(){

  }

  createCustomerForm(){
    return new Promise((resolve,reject)=>{
      import('../../customercreation/customercreation.component').then(({ CustomercreationComponent }) => {
        const componentFactory = this.componentFactoryResolver.resolveComponentFactory(CustomercreationComponent);
        resolve(this.createplaceholder?.createComponent(componentFactory));
      });
    })
    
  }

  getLocations(hierarchy,$event){
    let val;
    if($event == ''){val = $event}
    else{val = $event?.target?.value}

    
    this.customerService.fetchLocations(hierarchy,val).subscribe((data)=>{
      console.log(hierarchy,val,data.data.business_units)
      if(hierarchy == 'regions'){
        this.regions = data.data.regions
      }
      else if (hierarchy == 'business_unit'){
        this.business_units = data.data.business_units
        this.filter.buid = ''
        this.filter.servicecenter = ''
        
      }
      else if (hierarchy == 'servicecenter'){
        this.service_centers = data.data.service_centers
        this.filter.servicecenter = ''
      }
      
    })
  }

  resetFilter(){
    this.filter = new CustomerFilter()
  }

  getCustomers(activePage){
    
      this.store.dispatch(new FetchEcmiCustomers())
      this.ecmiCustomersList$ = this.ecmiCustomersList.subscribe((data) => {
        this.sharedService.setActiveCustomerPage(activePage)
        this.customersType = activePage
        this.activePage = activePage
        this.customers$ = data.customers//user.can_create_customers
        this.ecmi_total_customers = data.total_customers
        
      });
    
  }

  ngOnDestroy(){
    console.log("Customer component destroyed")
    this.emsCustomersList$?.unsubscribe()
    this.ecmiCustomersList$?.unsubscribe()
  }



}