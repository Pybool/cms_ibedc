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
  selector: 'app-todaycollectionsems',
  templateUrl: './todaycollectionsems.component.html',
  styleUrls: ['./todaycollectionsems.component.css']
})
export class TodaycollectionsemsComponent {
  emsheaders:string[] = ['Customer Name','Account No','Receipt No','Meter No','Pay Date','Payments','Business Unit','Trans Amount','Status Message','Pay ID','Trans ID']
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

    window.waitForElm('#postpaid-todaycols-spinner-wrapper').then((parentElement) => {
      this.spinnerService.showSpinner(parentElement);
      this.sharedService.setSpinnerText('Fetching data from source...')
      this.convertTableService.convertTable({id:'today-cols-payments-ems-history_table'})
    })

    this.paymentService.fetchTodayCollectionsEms().pipe(take(1)).subscribe((response)=>{
      console.log(response.data)

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
