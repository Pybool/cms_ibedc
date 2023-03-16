import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-billinginformation',
  templateUrl: './billinginformation.component.html',
  styleUrls: ['./billinginformation.component.css']
})
export class BillinginformationComponent implements OnInit {

  public bills
  JSON
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private customerService:CustomerService) 
  { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log("Account details ===> ", params)
      if(params?.accounttype=='postpaid'){
        this.customerService.fetchSingleCustomerBills(params).subscribe((response)=>{
          if (response.status){
            this.bills = response.data
            console.log(this.bills)
          }
          else{alert(response.message)}
        })
      }
      else{}
      
    });
  }

}
