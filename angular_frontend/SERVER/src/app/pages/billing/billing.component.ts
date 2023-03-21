import { Component, OnInit, Renderer2 } from '@angular/core';
import { of } from 'rxjs';
import { take } from 'rxjs/operators';
import { BillingService } from 'src/app/services/billing.service';
import { ConvertTableService } from 'src/app/services/convert-table.service';
import { SharedService } from 'src/app/services/shared.service';
import { SpinnerService } from 'src/app/services/spinner.service';

interface CustomWindow extends Window {
  
  waitForElm:(arg1) => any;
  DataTable:(arg1,arg2)=>void;
}

declare let window: CustomWindow;

@Component({
  selector: 'app-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.css']
})
export class BillingComponent implements OnInit {
  bills:any[];
  rawQueryUsed = false;
  headers:string[] = ['Customer Name', 'Account Number', 'Tarrif Code', 'Billing Date', 'Due Date', 'Consumption (kw/h)', 'Net Arrears', 'Total Due', 'Back Balance', 'BUID', 'BU Name', 'BM Mobile', 'CSO Mobile', 'Bill ID', 'Account Type', 'Bill Year', 'Bill Month', 'Previous Balance', 'Meter Number', 'Payment', 'Service Address 1', 'Service Address 2', 'Service Address 3', 'ADC', 'Adjustment', 'Dials', 'Energy Read Date', 'Minimum CHG Read Date', 'Minimum Current CHG', 'Present KWH', 'Previous KWH', 'Demand Read Date', 'Present Demand', 'Previous Demand', 'Multiplier', 'Consumption MD', 'Current KWH', 'Current MD', 'Rate', 'FC', 'MMF', 'Reconnection Fee', 'Last Pay', 'Current CHG Total', 'VAT', 'Customer Care', 'Old Account No', 'Vat No', 'Lar Date', 'Lar', 'Mobile', 'Last Pay Amount', 'Email', 'E-mail2', 'E-mail3', 'Is Selected', 'Is Confirmed', 'Is Sms Sent', 'Read Mode', 'Row Guid', 'Refund', 'Back Arrears', 'Back Charge', 'Back Kwh', 'B Vat', 'Net Back Arrears', 'Grand Total', 'Service Id', 'Band Adjustment']
  
  constructor(private renderer: Renderer2,
              private spinnerService: SpinnerService,
              private sharedService:SharedService,
              private convertTableService: ConvertTableService,
              private billingService: BillingService) { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
    this.sharedService.setActiveSearchInput('billing')
  }

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);

    window.waitForElm('#spinner-wrapper').then((parentElement) => {
      this.spinnerService.showSpinner(parentElement);
      this.sharedService.setSpinnerText('Fetching data from source...')
      this.convertTableService.convertTable({id:'billinghistory_table'})
    })

    this.billingService.fetchCustomersBilling().pipe(take(1)).subscribe((response)=>{
      console.log(response.data)
      if(response.rawQueryUsed == true){
        this.rawQueryUsed = true
      }
      this.bills = response.data
    })
  }

}
