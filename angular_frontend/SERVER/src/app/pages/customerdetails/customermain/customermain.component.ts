import { Component, OnInit, Renderer2 } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CaadService } from 'src/app/services/caad.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-customermain',
  templateUrl: './customermain.component.html',
  styleUrls: ['./customermain.component.css']
})
export class CustomermainComponent implements OnInit {

  accountno;
  accounttype;
  meterno;
  params:any = {}
  constructor(private route: ActivatedRoute, 
    private sharedService:SharedService,
    private caadService:CaadService) { }

  ngOnInit(): void {
    
    this.route.queryParams.subscribe(params => {
      this.params = params
      console.log("Customer landing page details ===> ", params)
      this.accountno = params?.accountno
      this.accounttype = params?.accounttype
      this.meterno = params?.meterno
    })
  }


  navigateToPage($event,base){
    console.log(base)
    // console.log('customer/information/basic-information')
    this.sharedService.navigateWithParams(base,this.params)
  }

  loadCaad($event,base){
    this.caadService.setListOrCreate(false)
    this.sharedService.navigateWithParams(base,this.params)
  }

}
