import { Component,OnDestroy  } from '@angular/core';
import { Store } from '@ngrx/store';
import { take } from 'rxjs/operators';
import { CaadService } from 'src/app/services/caad.service';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';
import { ApproveCaad } from '../customerdetails/caad/state/customercaad.actions';
import { caadApprovalData } from './state/caad.selector';
import { FetchCaadList } from './state/caadlist.actions';

@AutoUnsubscribe
@Component({
  selector: 'app-caadlist',
  templateUrl: './caadlist.component.html',
  styleUrls: ['./caadlist.component.css']
})
export class CaadlistComponent implements OnDestroy {
  header;
  approvalList = [];
  lineItems = []
  approvers = []
  loadedCaadRecord;
  activeCustomer:any = {}
  is_metered:boolean = true;
  typeLineItem
  caad_roles_list = ['BHM','CCO','OC','RPU']
  position = 'BHMX'
  customer:any = {}
  ref:any;
  sebm = `NGN 0.00`
  tebm= `NGN 0.00`
  tebmRaw:number;
  selectedVat;
  refundAmount:any = '';
  refundAmountRaw:any =0.00 ;
  totalEstimate:any = '';
  vats:any = [{name:2.5},{name:5.5},{name:7.5}]
  
  constructor(private store :Store,private caadService: CaadService,){
    this.store.dispatch(new FetchCaadList())
  }

  ngOnInit(){
    this.store.select(caadApprovalData).pipe(take(2)).subscribe((response)=>{
      console.log(response)
      if(response.data?.status){
        this.approvalList = response.data?.data
      }
    })
 
  }

  submit(){

  }

  trackByFn(){

  }

  getItemByKey(array, id) {
    return array.find(item => item.id == id);
  }

  viewCaadRecord($event,id){
    this.caadService.fetchCaadLineItems(id).subscribe((response)=>{
      if(response.status){
        this.header = id
        this.lineItems = response.data
        console.log(response.approvers)
        this.approvers = response.approvers
        console.log(this.lineItems)
        const sebmRaw = this.lineItems.reduce((acc, obj) => acc + (obj.ebm || 0), 0);
        this.sebm = `NGN ${sebmRaw.toLocaleString('en-US')}`
        let activeHeader = this.getItemByKey(this.approvalList,id)
        this.tebm = `NGN ${activeHeader.total_accrued.toLocaleString('en-US')}` 
        this.refundAmount =  `NGN ${activeHeader.refund_amount.toLocaleString('en-US')}`
      }
    })
    document.getElementById('caad_approval').classList.add("content-active")
  }

  approveCaad($event){
    this.store.dispatch(new ApproveCaad(this.header))
  }

  revertCaad($event){
    let comment = window.prompt('Enter a comment to decline this record')
    if (comment){
      console.log(comment)
      this.caadService.caadApproval(this.header,0,comment).pipe(take(1)).subscribe((response)=>{
        console.log(response)
      })
    }

  }

  exit($event){
    document.getElementById('caad_approval').classList.remove("content-active")
  }

  ngOnDestroy(): void {
    
  }
}
