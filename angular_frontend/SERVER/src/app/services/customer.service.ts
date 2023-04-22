import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { UserState } from '../authentication/state/auth.selector';
import { AppState } from '../basestore/app.states';
import { ecmiCustomers, emsCustomers } from '../pages/customersmodule/prepaidcustomers/state/customer.selector';
import { UserModifyModel } from '../pages/user/createuser/models/user';
import { map, switchMap, take, tap } from 'rxjs/operators';
import { SharedService } from './shared.service';
let self;

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  singleCustomer:Observable<any>;
  customerId;
  cachedData$
  data$
  userState
  permission_hierarchy;
  emsCustomersList;
  ecmiCustomersList;
  emsCustomersList$;
  ecmiCustomersList$;
  customer;
  dual:boolean = false
  newCustomerList;
  kanban = false;
  newCustomerList$:any = new BehaviorSubject<any>({});
  
  private readonly cacheTimeMs = 5 * 60 * 1000; // Cache for 5 minutes

  constructor(private store: Store<AppState>,
              private http: HttpClient,private router: Router,
              private sharedService: SharedService) { 
    this.userState = this.store.select(UserState);
    self = this
  }

   getCurrentDate() {
    const date = new Date();
    const year = date.getFullYear();
    const month = this.padNumber(date.getMonth() + 1);
    const day = this.padNumber(date.getDate());
    const hours = '00';
    const minutes = '00';
    const seconds = '00';
    return `${year}:${month}:${day} ${hours}:${minutes}:${seconds}`;
  }
  
  padNumber(num) {
    return num.toString().padStart(2, '0');
  }

  toggleView(){
    const tablewraps:any = document.querySelector("#table-wraps")
    const kanbanwraps:any = document.querySelector("#kanban-wraps")
    if(this.kanban){
      this.kanban = false;
      kanbanwraps.style.display = 'none'
      tablewraps.style.display = 'block'
      localStorage.setItem('cust_view_mode','list')
    }
    else{
      this.kanban = true
      tablewraps.style.display = 'none'
      kanbanwraps.style.display = 'flex'
      localStorage.setItem('cust_view_mode','grid')
    }
  }

  swapCustomerlist(data){
    console.log(data,self)
    self.newCustomerList = data
    self.newCustomerList$.next(data)
    console.log(self.newCustomerList)
  }

  public getNewCustomerList(){
    return this.newCustomerList$.asObservable()
  }

  nextPage(page,type){
    return this.http.get(`${environment.api}/customers/${type}?start_date=${this.getCurrentDate()}&end_date=${this.getCurrentDate()}&limit=100&offset=${parseInt(page)*100}&permission_hierarchy=${this.permission_hierarchy}`)
  }
  
  
  fetchcustomers(type:string):Observable<any>{
    this.userState.pipe(
      take(1)
    ).subscribe((user) => {
      this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
      
    });
    const currentTime = new Date().getTime();
    
      switch (type){
        case 'postpaid':
          // this.cachedData$ = this.store.select(emsCustomers);
          // this.cachedData$.subscribe((data) => {
          //   console.log("checking cache ===> ",!data.customers || (data?.timestamp || 0), this.cacheTimeMs, currentTime)
          //   if (!data.customers || (data?.timestamp || 0) + this.cacheTimeMs < currentTime) {
              return this.http.get(`${environment.api}/customers/postpaid?start_date=${this.getCurrentDate()}&end_date=${this.getCurrentDate()}&permission_hierarchy=${this.permission_hierarchy}`)
          //   }
          //   return of(this.cachedData$)
          // })
          // return this.data$
          
          
          case 'prepaid':
            // return this.http.get(`${environment.api}/customers/prepaid?start_date=${this.getCurrentDate()}&end_date=${this.getCurrentDate()}&permission_hierarchy=${this.permission_hierarchy}`).pipe(
            //   map((newData) => {
            //     newData['timestamp'] = new Date().getTime()
            //     return newData
            //   })
            // );
            this.cachedData$ = this.store.select(ecmiCustomers);
            return this.cachedData$.pipe(
              switchMap((data:any) => {
                const currentTime = new Date().getTime();
                if ((currentTime - data?.timestamp) > this.cacheTimeMs) {
                  return this.http.get(`${environment.api}/customers/prepaid?start_date=${this.getCurrentDate()}&end_date=${this.getCurrentDate()}&permission_hierarchy=${this.permission_hierarchy}`).pipe(
                    map((newData) => {
                      newData['timestamp'] = new Date().getTime()
                      return newData
                    })
                  );
                } else {
                  return of(data.customers);
                }
              })
            );
          
          
          
      }
  }
   
  getItemById(array, accountno) {

    return array?.find(item => item.accountno == accountno);
  }

  fetchSinglecustomer(payload){
    /*First search in customers list store */    
    switch (payload?.accounttype){
      case 'postpaid':
        this.emsCustomersList = this.store.select(emsCustomers);
        this.emsCustomersList$ = this.emsCustomersList.subscribe((data) => {
          this.customer = this.getItemById(data.customers,payload.accountno) 
          console.log("Found customer in store ", this.customer)
          
        });   
        break;
      
      case 'prepaid':
        this.ecmiCustomersList = this.store.select(ecmiCustomers);
        this.ecmiCustomersList$ = this.ecmiCustomersList.subscribe((data) => {
          this.customer = this.getItemById(data.customers,payload.accountno) 
          console.log("Found customer in store ", this.customer)
          
        }); 
        break;
    }

    if (this.customer){
      return of({status:true,data:this.customer})
    }
    
    /*next searching in search results store if not in customers list store */
    /*Send a fresh request to backend to fetch customer data if not found in store */
    return this.http.get<any>(`${environment.api}/customer/information/basic-information?accounttype=${payload?.accounttype}&accountno=${payload?.accountno}`)
  }

  fetchSingleCustomerBills(payload){
    return this.http.get<any>(`${environment.api}/singlecustomer-bills?accounttype=${payload?.accounttype}&accountno=${payload?.accountno}&page=${1}`)
  }

  fetchSingleCustomerPayments(payload){
    const customerUID = payload?.accounttype === 'prepaid' ? payload?.meterno : payload.accountno;
    return this.http.get<any>(`${environment.api}/singlecustomer-payments?accounttype=${payload?.accounttype}&accountno=${customerUID}&page=${1}`)
  }

  fetchSingleCustomerMetering(payload){
    return this.http.get<any>(`${environment.api}/singlecustomer-meteringInfo?accounttype=${payload?.accounttype}&accountno=${payload?.accountno}`)
  }

  fetchSingleCustomerAssets(payload){
    return this.http.get<any>(`${environment.api}/singlecustomer-assets?accounttype=${payload?.accounttype}&accountno=${payload?.accountno}`)
  }

  // /singlecustomer-assets?accountno=12/28/52/1258-01&accounttype=postpaid
  fetchLocations(hierarchy:string,q:string){
    return this.http.get<any>(`${environment.api}/locations/getdata?hierarchy=${hierarchy}&q=${q}`)
  }

  deepFetchCustomers(payload):Observable<any>{
    console.log("Deep search payload ===> ", payload)
    this.userState.subscribe((user) => {
      this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
      
    });    
    return  this.http.post(`${environment.api}/searching/prepaid/customers?permission_hierarchy=${this.permission_hierarchy}`,payload)

  }

  deepEmsFetchCustomers(payload):Observable<any>{
    console.log("Deep search payload ===> ", payload)
    this.userState.subscribe((user) => {
      this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
      
    });    
    return  this.http.post(`${environment.api}/searching/postpaid/customers?permission_hierarchy=${this.permission_hierarchy}`,payload)

  }

  advancedFilterEcmiCustomers(payload):Observable<any>{
    this.sharedService.getDualSearchState().pipe(take(1)).subscribe((state)=>{
      this.dual = state
    })
    console.log("Advanced filtering payload ===> ", payload)
    this.userState.subscribe((user) => {
      this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
      
    });    
    return  this.http.post(`${environment.api}/advancedsearching/prepaid/customers?permission_hierarchy=${this.permission_hierarchy}&dual=${this.dual}`,payload)

  }

  advancedFilterEmsCustomers(payload):Observable<any>{
    this.sharedService.getDualSearchState().pipe(take(1)).subscribe((state)=>{
      this.dual = state
    })
    console.log("Advanced filtering payload ===> ", payload)
    this.userState.subscribe((user) => {
      this.permission_hierarchy = user.permission_hierarchy//user.can_create_customers
      
    });    
    return  this.http.post(`${environment.api}/advancedsearching/postpaid/customers?permission_hierarchy=${this.permission_hierarchy}`,payload)

  }

  fecthCustomerFormMetadata(){
    return this.http.get<any>(`${environment.api}/cms/customerform/metadata?as_method=${true}`)
    
  }

  initiateCaad(payload){
    console.log(payload)
    return this.http.post<any>(`${environment.api}/cms/customer/initiate-caad`,payload)
    
  }

}
