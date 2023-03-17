import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnInit,AfterViewInit, Renderer2, ViewChild, ViewContainerRef } from '@angular/core';
import { customerData } from './customerdata.js'
import { abbreviateName } from '../../../utils'
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
import { Router } from '@angular/router';
import { NgZone } from '@angular/core';
import { map, tap } from 'rxjs/operators';
import { DataTablesModule } from 'angular-datatables';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';

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
export class CustomersComponent implements OnInit, AfterViewInit {
  public metaData;
  dtOptions: DataTables.Settings = {};
  dtTrigger: Subject<any> = new Subject<any>();
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
  datatableSource
  // dtOptions: DataTables.Settings = {};
  @ViewChild('editcustomerplaceholder', { read: ViewContainerRef }) placeholder: ViewContainerRef;
  @ViewChild('createcustomerplaceholder', { read: ViewContainerRef }) createplaceholder: ViewContainerRef;
  constructor(private store: Store<AppState>,
              private zone: NgZone,
              private sharedService:SharedService,
              private cd: ChangeDetectorRef,
              private customerService:CustomerService,
              private componentFactoryResolver: ComponentFactoryResolver,
              private renderer: Renderer2) { 
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
        // Update UI here
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
    
    this.userState.subscribe((user) => {
      this.can_create_customers = user.can_create_customer
    });

    this.ecmiCustomersList$ = this.ecmiCustomersList.subscribe((data:any) => {
        this.sharedService.setActiveCustomerPage('prepaid')
        this.customersType = 'prepaid'
        this.activePage = 'prepaid'
        this.customers$ = of(data.customers)//user.can_create_customers
        this.ecmi_total_customers = data.total_customers
        this.datatableSource = data.customers
        console.log("=====> Done setting ECMI customers ",this.ecmi_total_customers)
        
     })
  

    }

    loadScript(src) {
      const script = this.renderer.createElement('script');
      script.type = 'text/javascript';
      script.src = src;
      this.renderer.appendChild(document.body, script);
    }
 
  loadCustomerInformation($event,accountno,accounttype){
    let base = `customer/information/basic-information`
    const queryParams = {accountno : accountno, accounttype: accounttype?.toLowerCase() };
    this.sharedService.navigateWithParams(base,queryParams)
  }

  openCustomerCreateForm(){
    this.createCustomerForm().then((status)=>{
        document.getElementById('create_customer').classList.add("content-active")
      console.log(document.getElementById('create_customer').classList)
      document.getElementById('create_customer').classList.add("content-active")
      
    })
    this.sharedService.setFormHeader('Create Awaiting Customer')
    this.mode = 'create'
    
  }

  openCustomerUpdateForm($event){
    this.currentAccountno = $event.target.closest('td').id
    console.log("Account no ===> ", this.currentAccountno)
    this.openCustomerCreateForm()//Bug
    this.sharedService.setFormHeader(['edit','Update Existing Customer',this.activePage,this.currentAccountno])
    this.mode = 'edit'
  }

  convertTable(){
    try{
      setTimeout(()=>{
        if(this.datatableSource && this.datatableSource.length > 0){
          this.datatableElement.dtInstance.then((dtInstance: DataTables.Api) => {
            // Convert the table to a datatable here
            dtInstance.destroy();
            this.datatableElement.dtTrigger.next();
          });
        }
        // }
        // window.waitForElm('#customer_table').then((elm) => {
        //   console.log("Table el =----> ", elm)
        //     let table = new window.DataTable('#customer_table', {
        //         destroy: true,"pageLength": 10,"bPaginate": false,
        //         "responsive": true,
        //         "processing": true,
        //         "searching":false,
                
        //     });
        // });
      },1000)
      
      }
  catch(err){ }
  }

  ngAfterViewInit(){
    this.convertTable()
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

  submitFilter(){
    console.log("Customer filter ",this.filter)
  }

  getRegions(){

  }

  createCustomerForm(){
    return new Promise((resolve,reject)=>{
      import('./../customercreation/customercreation.component').then(({ CustomercreationComponent }) => {
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
    if (this.activePage == 'prepaid'){
      this.store.dispatch(new FetchEmsCustomers())
      this.emsCustomersList = this.store.select(emsCustomers);
      this.emsCustomersList$ = this.emsCustomersList.subscribe((data) => {
        this.sharedService.setActiveCustomerPage(activePage)
        this.customersType = activePage
        this.activePage = activePage
        this.customers$ = of(data.customers)
        this.ems_total_customers = data.total_customers
        
      });
    }
    else{
      try{
        this.emsCustomersList$.unsubscribe()
      }
      catch{}
      this.store.dispatch(new FetchEcmiCustomers())
      this.ecmiCustomersList$ = this.ecmiCustomersList.subscribe((data) => {
        this.sharedService.setActiveCustomerPage(activePage)
        this.customersType = activePage
        this.activePage = activePage
        this.customers$ = data.customers//user.can_create_customers
        this.ecmi_total_customers = data.total_customers
        
      });
    }
  }

  ngOnDestroy(){
    console.log("Customer component destroyed")
    this.emsCustomersList$?.unsubscribe()
    this.ecmiCustomersList$?.unsubscribe()
  }



}
