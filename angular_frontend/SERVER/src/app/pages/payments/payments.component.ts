import { Component, OnInit, Renderer2 } from '@angular/core';
import { take } from 'rxjs/operators';
import { ConvertTableService } from 'src/app/services/convert-table.service';
import { PaginationService } from 'src/app/services/pagination.service';
import { PaymentsService } from 'src/app/services/payments.service';
import { SharedService } from 'src/app/services/shared.service';
import { SpinnerService } from 'src/app/services/spinner.service';

interface CustomWindow extends Window {
  
  waitForElm:(arg1) => any;
  DataTable:(arg1,arg2)=>void;
}

declare let window: CustomWindow;

@Component({
  selector: 'app-payments',
  templateUrl: './payments.component.html',
  styleUrls: ['./payments.component.css']
})
export class PaymentsComponent implements OnInit {
  ecmi_payments:boolean = true
  ecmiheaders:string[] = ['Customer Name','Account No','Transaction Ref','Token','Meter No','Trans Date','Amount','Business Unit','Units','Trans Amount','Cost of Units','Status Message','CSPClientId','Day','FC','KVA','MMF','MeterNo','OperatorId','Reasons','TokenType','TotalCount','TransactionComplete','TransactionDateTime','TransactionNo','TransactionType','VAT','Year','EnteredBy','PaymentType','Status','Status1','TransactionResponseMessage']
  payments:any[] = []
  Math;
  startDate = null;
  endDate = null;
  constructor(private renderer: Renderer2,
    private spinnerService: SpinnerService,
    private sharedService:SharedService,
    private convertTableService: ConvertTableService,
    private paginationService : PaginationService,
    private paymentService: PaymentsService) { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
    this.sharedService.setActiveSearchInput('ecmipayments')
  }

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);

    window.waitForElm('#payments-spinner-wrapper').then((parentElement) => {
      this.spinnerService.showSpinner(parentElement);
      this.sharedService.setSpinnerText('Fetching data from source...')
      this.convertTableService.convertTable({id:'paymentshistory_table'})
    })

    this.paymentService.fetchCustomersPayments().pipe(take(1)).subscribe((response)=>{
      console.log(response)
      if(response.status){
        this.paginationService.setLinks(response.next,response.last,'prepaidpayments')
        this.payments = response.data
      }
      else{this.spinnerService.hideSpinner();alert(response?.message)}
    })
  }

  handler($event){
    
    if ($event.target.name=='start_date'){
        this.startDate = $event.target.value
        document.querySelector('#disabled-date').removeAttribute('disabled')
    }
    if ($event.target.name=='end_date'){
        this.endDate = $event.target.value
    }

    console.log(this.startDate, this.endDate)
 
    if (this.startDate!=null && this.endDate!=null){
        console.log("Firring event ....")
        this.searchDatePayments()

    }

}

  searchDatePayments(){
    const payload = {type:'ecmi',start_date:this.startDate,end_date:this.endDate}
    this.paymentService.searchDatePaymentsHistory(payload).pipe(take(1)).subscribe((response)=>{
      console.log(response)
      if(response.status){
        this.payments = response.data
      }
      else{this.spinnerService.hideSpinner();alert(response?.message)}
      
    })
  }

  loadCustomerInformation($event,accountno,meterno,accounttype){
    let base = `customer/information/basic-information`
    const queryParams = {accountno : accountno, accounttype: accounttype?.toLowerCase(),meterno:meterno };
    this.sharedService.navigateWithParams(base,queryParams)
  }

  


}
