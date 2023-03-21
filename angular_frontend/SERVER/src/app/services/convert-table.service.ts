import { Injectable } from '@angular/core';
import { SharedService } from './shared.service';
import { SpinnerService } from './spinner.service';
interface CustomWindow extends Window {
  waitForElm:(arg1) => any;
  DataTable: (searchTerm: string,{}) => void;
}

declare let window: CustomWindow;

@Injectable({
  providedIn: 'root'
})
export class ConvertTableService {
  intervalId
  constructor(private sharedService: SharedService, private spinnerService:SpinnerService) { }

  convertTable(args){
    return new Promise((resolve, reject)=>{
      try{
        const allowedTime =  1 * 60 * 1000; // Wait for 60 seconds
        const start_time = new Date().getTime()
        this.intervalId = setInterval(() => {
          let len = document.querySelector('tbody')?.querySelectorAll('tr')?.length
  
          if ((new Date().getTime() - start_time) > allowedTime) {
            
            console.log("Terminated fetching as it took too long")
            this.spinnerService.hideSpinner();
            return clearInterval(this.intervalId);
          }
          if(len > 0){
            window.waitForElm(`#${args.id}`).then((elm) => {
              this.sharedService.setSpinnerText('Constructing data table...')
              new window.DataTable(`#${args.id}`, {
                    destroy: true,"pageLength": 10,"bPaginate": false,
                    "responsive": true,
                    "processing": true,
                    "searching":false,
                    "deferRender": true, 
                    "order": []
                });
  
                clearInterval(this.intervalId);
                this.spinnerService.hideSpinner();
                let t:any = elm
                t.style.opacity = '1'
                resolve(true)
            });
          }
        }, 100);
       
        }
      catch(err){ }
    })
    
  }
 
}
