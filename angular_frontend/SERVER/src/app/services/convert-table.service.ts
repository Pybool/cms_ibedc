import { Injectable } from '@angular/core';
import { SharedService } from './shared.service';
import { SpinnerService } from './spinner.service';
import { interval } from 'rxjs';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';

interface CustomWindow extends Window {
  waitForElm:(arg1) => any;
  DataTable: (searchTerm: string,{}) => void;
}
declare let window: CustomWindow;
var tableObj = null

@Injectable({
  providedIn: 'root'
})
@AutoUnsubscribe
export class ConvertTableService {
  intervalId = null
  constructor(private sharedService: SharedService, private spinnerService:SpinnerService) { }

  convertTable(args){
    return new Promise((resolve, reject)=>{
      var subscription
      if(tableObj!=null){
        console.log(tableObj)
        tableObj.clear();
        // tableObj.destroy();
        // $(`#${args.id}` + " tbody").empty();
        // $(`#${args.id}` + " thead").empty();
        }
        
      
      try{
          subscription = interval(100).subscribe(() => {
          let len = document.querySelector('tbody')?.querySelectorAll('tr')?.length
          if(len > 0){
            
            window.waitForElm(`#${args.id}`).then((elm) => {
              

               
              this.sharedService.setSpinnerText('Constructing data table...')
              console.log("Table obj ----> ", tableObj)
              tableObj = new window.DataTable(`#${args.id}`, {
                    destroy: true,"pageLength": 10,"bPaginate": false,
                    "responsive": true,
                    "processing": true,
                    "searching":false,
                    "deferRender": true, 
                    "order": []
                });
                this.spinnerService.hideSpinner();
                let t:any = elm
                t.style.opacity = '1'
                subscription?.unsubscribe()
                resolve(true)
            });
          }
        });
      
      }
      catch(err){subscription?.unsubscribe()}
    })
    
  }
 
}
