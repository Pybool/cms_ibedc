import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-paymentsinformation',
  templateUrl: './paymentsinformation.component.html',
  styleUrls: ['./paymentsinformation.component.css']
})
export class PaymentsinformationComponent implements OnInit {
  payments:any = []
  accounttype;
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private customerService:CustomerService) 
  { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log("Account details ===> ", params)
      if(params?.accounttype=='postpaid'){
        this.accounttype=params?.accounttype
        this.customerService.fetchSingleCustomerPayments(params).subscribe((response)=>{
          if (response.status){
            this.payments = response.data
            console.log(this.payments)
          }
          else{alert(response.message)}
        })
      }
      else{}
      
    });
  }

}
