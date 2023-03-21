import { Component,Renderer2, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';
import { DataTablesModule } from 'angular-datatables';
import { SpinnerService } from 'src/app/services/spinner.service';
import { ConvertTableService } from 'src/app/services/convert-table.service';

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
  message=''
  intervalId
  dtOptions: DataTables.Settings = {};
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private renderer: Renderer2,
    private customerService:CustomerService,
    private spinnerService:SpinnerService,
    private convertTableService:ConvertTableService) 
  { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');

    this.route.queryParams.subscribe(params => {
      console.log("Account details ===> ", params)
      this.customerService.fetchSingleCustomerBills(params).subscribe((response)=>{
        if (response.status){
          this.bills = response.data
          window.waitForElm('#billswrapper').then((parentElement) => {
            this.spinnerService.showSpinner(parentElement);
            this.sharedService.setSpinnerText('Fetching data from source...')
            this.convertTableService.convertTable({id:'cust_bills'})
          })
        }
        else{
          console.log(response.status)
          this.spinnerService.hideSpinner();
          this.message=response.message;
          this.bills = false}
      })
    });
  }

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);
  }

  ngAfterViewInit(){
    
    
  }

 

}
