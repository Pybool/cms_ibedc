import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-customermain',
  templateUrl: './customermain.component.html',
  styleUrls: ['./customermain.component.css']
})
export class CustomermainComponent implements OnInit {

  accountno;
  accounttype;
  params
  constructor(private route: ActivatedRoute, private sharedService:SharedService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.params = params
      console.log("Customer landing page details ===> ", params)
      this.accountno = params?.accountno
      this.accounttype = params?.accounttype

    })
  }

  navigateToPage($event,base){
    console.log(base)
    // console.log('customer/information/basic-information')
    this.sharedService.navigateWithParams(base,this.params)
  }

}
