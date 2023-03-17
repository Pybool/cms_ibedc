import { Component,Renderer2, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';
import { DataTablesModule } from 'angular-datatables';

interface CustomWindow extends Window {
  
  waitForElm:(arg1) => any;
  DataTable:(arg1,arg2)=>void;
}

declare let window: CustomWindow;


@Component({
  selector: 'app-billinginformation',
  templateUrl: './billinginformation.component.html',
  styleUrls: ['./billinginformation.component.css']
})
export class BillinginformationComponent implements OnInit {

  public bills
  JSON
  dtOptions: DataTables.Settings = {};
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private renderer: Renderer2,
    private customerService:CustomerService) 
  { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');

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

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);
  }

  ngAfterViewInit(){
    try{
      window.waitForElm('#cust_bills').then((elm) => {
        console.log("Table el =----> ", elm)
          let table = new window.DataTable('#cust_bills', {
              destroy: true,"pageLength": 10,"bPaginate": true,
              "responsive": true,
              "processing": true,
              "searching":false,
              
          });
      });
      }
  catch(err){ }
  }

}
