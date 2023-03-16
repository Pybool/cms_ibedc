import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-meteringinformation',
  templateUrl: './meteringinformation.component.html',
  styleUrls: ['./meteringinformation.component.css']
})
export class MeteringinformationComponent implements OnInit {

  accounttype;
  meterData;
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private customerService:CustomerService) 
  { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log("Metering  details ===> ", params)
      this.accounttype=params?.accounttype
      this.customerService.fetchSingleCustomerMetering(params).subscribe((response)=>{
        if (response.status){
          this.meterData = response.data[0]
          console.log(this.meterData)
        }
        else{alert(response.message)}
      })
      
    });
  }
  // fetchSingleCustomerMetering
}
