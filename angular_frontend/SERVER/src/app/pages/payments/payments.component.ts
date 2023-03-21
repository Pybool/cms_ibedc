import { Component, OnInit, Renderer2 } from '@angular/core';
import { take } from 'rxjs/operators';
import { ConvertTableService } from 'src/app/services/convert-table.service';
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
  emsheaders:string[] = ['Pay ID','Trans ID','Receipt No','Account No','Meter No','Pay Date','Payments','Business Unit','Trans Amount','Status Message']
  ecmiheaders:string[] = ['Customer Name','Transaction Ref','Token','Meter No','Account No','Trans Date','Amount','Business Unit','Units','Trans Amount','Cost of Units','Status Message','CSPClientId','Day','FC','KVA','MMF','MeterNo','OperatorId','Reasons','TokenType','TotalCount','TransactionComplete','TransactionDateTime','TransactionNo','TransactionType','VAT','Year','EnteredBy','PaymentType','Status','Status1','TransactionResponseMessage']
  payments:any[] = []
  Math;
  constructor(private renderer: Renderer2,
    private spinnerService: SpinnerService,
    private sharedService:SharedService,
    private convertTableService: ConvertTableService,
    private paymentService: PaymentsService) { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
    this.sharedService.setActiveSearchInput('payments')
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
      console.log(response.data)
      this.payments = response.data
    })
  }

  


}
