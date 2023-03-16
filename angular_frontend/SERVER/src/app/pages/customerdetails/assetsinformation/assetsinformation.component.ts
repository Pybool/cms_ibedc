import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-assetsinformation',
  templateUrl: './assetsinformation.component.html',
  styleUrls: ['./assetsinformation.component.css']
})
export class AssetsinformationComponent implements OnInit {
  assetsData;
  accounttype;
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,

    private customerService:CustomerService) 
  { }

  // http://127.0.0.1:4200/customer/information/basic-information?accountno=18%2F56%2F28%2F9310-01&accounttype=Prepaid  this customer has no dss_id handle the error

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      console.log("Assets  details ===> ", params)
      this.accounttype=params?.accounttype
      this.customerService.fetchSingleCustomerAssets(params).subscribe((response)=>{
        if (response.status){
          this.assetsData = response.data[0]
          console.log(this.assetsData)
        }
        else{alert(response.message)}
      })
      
    });
  }

}
