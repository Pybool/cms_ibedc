import { Component, OnInit, Renderer2 } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { SharedService } from 'src/app/services/shared.service';
import { DataTablesModule } from 'angular-datatables';
import { SpinnerService } from 'src/app/services/spinner.service';
import { ConvertTableService } from 'src/app/services/convert-table.service';
import Swal from 'sweetalert2';


interface CustomWindow extends Window {
  
  waitForElm:(arg1) => any;
  DataTable:(arg1,arg2)=>void;
}

declare let window: CustomWindow;

@Component({
  selector: 'app-paymentsinformation',
  templateUrl: './paymentsinformation.component.html',
  styleUrls: ['./paymentsinformation.component.css']
})
export class PaymentsinformationComponent implements OnInit {
  payments:any = []
  accounttype;
  message
  dtOptions: DataTables.Settings = {};
  intervalId
  constructor(private store: Store<AppState>,
    private sharedService:SharedService,
    private route: ActivatedRoute,
    private customerService:CustomerService,
    private renderer: Renderer2,
    private spinnerService: SpinnerService,
    private convertTableService:ConvertTableService) 
  { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
    this.route.queryParams.subscribe(params => {
        this.accounttype=params?.accounttype
        this.customerService.fetchSingleCustomerPayments(params).subscribe((response)=>{
          if (response.status){
            this.payments = response.data
            console.log(this.payments)
          }
          else{
            Swal.fire({
              position: 'top-end',
              icon: 'error',
              title: `Customer payments!`,
              text:`${response?.message}`,
              showConfirmButton: false,
              timer: 1500
            })
              this.spinnerService.hideSpinner();
               this.message=response.message;this.payments = false
              }
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
    window.waitForElm('#wrapper').then((parentElement) => {
      this.spinnerService.showSpinner(parentElement);
      this.sharedService.setSpinnerText('Fetching data from source...')
      this.convertTableService.convertTable({id:'customer_payment_history'})
    })
    
  }

}
