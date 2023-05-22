import { Component, OnInit, Renderer2 } from '@angular/core';
import { take } from 'rxjs/operators';
import { ApprovalBoardService } from 'src/app/services/approvalboard.service';
import { ConvertTableService } from 'src/app/services/convert-table.service';
import { SharedService } from 'src/app/services/shared.service';
import { SpinnerService } from 'src/app/services/spinner.service';
import {download, exportSingle} from './record.exporter.js'

interface CustomWindow extends Window {
  
  waitForElm:(arg1) => any;
  DataTable:(arg1,arg2)=>void;
}

declare let window: CustomWindow;

@Component({
  selector: 'app-approvalboard',
  templateUrl: './approvalboard.component.html',
  styleUrls: ['./approvalboard.component.css']
})
export class ApprovalboardComponent implements OnInit {
  customers:any[] = []
  active:string = ''
  exportAccountNo:string;
  constructor(
    private sharedService:SharedService,
    private renderer: Renderer2,
    private spinnerService:SpinnerService,
    private convertTableService:ConvertTableService,
    private approvalBoardService: ApprovalBoardService)  { }

  ngOnInit(): void {
    this.loadScript('https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.js');
  }

  getPendingCustomers($event,action){
    this.active = action
    console.log(Object.keys($event.target))
    const tabs:any = document.querySelectorAll('.cardtab')
    tabs.forEach((tab)=>{
      tab.style.borderBottom = "thick solid #FFFFFF"
    })
    $event.target.closest('.cardtab').style.borderBottom = "thick solid #FF7518"
    const idsObj = {'pending':'pending_edits_widget_history_table','approved':'approved_edits_widget_history_table','declined':'declined_edits_widget_history_table'}
    this.approvalBoardService.fetchPendingCustomers(action).subscribe((response)=>{
      console.log(response)
      this.customers = response.data
      const tableWidget:any = document.querySelector(`#${idsObj[action]}`)
      tableWidget.style.display = 'block'
      window.waitForElm('#pendingcustwrapper').then((parentElement) => {
        this.spinnerService.showSpinner(parentElement);
        this.sharedService.setSpinnerText('Fetching data from source...')
        this.convertTableService.convertTable({id:idsObj[action]})
        
      })
    })
  }

  loadScript(src) {
    const script = this.renderer.createElement('script');
    script.type = 'text/javascript';
    script.src = src;
    this.renderer.appendChild(document.body, script);
  }

  highlightRow(e){
    const self = e.target
    e.stopPropagation()
    const bgColor = String($(self).closest('tr').css('backgroundColor'))
    if(bgColor != 'rgb(135, 206, 250)' && $(self).is(':checked')){
        $(self).closest('tr').css("background-color", "rgb(135, 206, 250)");
        $(self).closest('tr').find('td').each((col,td)=>{
            $(td).css("background-color", "rgb(135, 206, 250)");
            $(td).css("color", "rgb(255, 255, 255)");
        })
    }
    else{
        $(self).closest('tr').css("background-color", "rgb(255, 255, 255)");
        $(self).closest('tr').find('td').each((col,td)=>{
            $(td).css("background-color", "rgb(255, 255, 255)");
            $(td).css("color", "#8094ae");
        })
    }
    
}

download($event,id,accountno){
  this.exportAccountNo = accountno
  download(id,accountno)
}

exportSingle(type){
  this.approvalBoardService.getSingleCustomer(this.exportAccountNo,this.active).pipe(take(1)).subscribe((response)=>{
    if(response.status){
      exportSingle(type,response.data,this.getfileName(this.active))
    }
  })
  
}

getfileName(action){
  let currentDate = new Date().toISOString()
  const filenames = {'approved':'Approved Customers','pending':'Pending Customers','declined':'Declined Customers','created':'Created Customers'}
  return filenames[action] + '@' + currentDate
}

}
