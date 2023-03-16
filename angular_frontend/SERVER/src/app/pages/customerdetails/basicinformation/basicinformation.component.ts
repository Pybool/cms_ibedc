import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { SharedService } from 'src/app/services/shared.service';
import { ActivatedRoute } from '@angular/router';
import { LoadEmsCustomer } from '../../customers/state/customer.actions';
import { CustomerService } from 'src/app/services/customer.service';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-basicinformation',
  templateUrl: './basicinformation.component.html',
  styleUrls: ['./basicinformation.component.css']
})
export class BasicinformationComponent implements OnInit {
  customer;
  getCustomer;
  accountno;
  accounttype;
  constructor(private store: Store<AppState>,
              private sharedService:SharedService,
              private route: ActivatedRoute,
              private customerService:CustomerService) 
            { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log("Account details ===> ", params)
      // if(params?.accounttype=='postpaid'){
        // this.store.dispatch(new LoadEmsCustomer(params))
        this.customerService.fetchSinglecustomer(params).subscribe((response)=>{
          console.log(response)
          if (response.status){
            this.customer = response.data[0] || response.data
          }
          else{alert(response.message)}
        })
      // }
      // else{}
      
    });
    

  }

}
