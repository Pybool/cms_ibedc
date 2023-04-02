import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { CustomerService } from 'src/app/services/customer.service';
import { CustomerCaadService } from 'src/app/services/customercaad.service';
import { NotificationService } from 'src/app/services/notification.service';
import { SharedService } from 'src/app/services/shared.service';
import {MeteredCaadLineItem, IMeteredCaadLineItem, IUNMeteredCaadLineItem, UnmeteredCaadLineItem} from './caad.models'
import { CreateCaad } from './state/customercaad.actions';

@Component({
  selector: 'app-caad',
  templateUrl: './caad.component.html',
  styleUrls: ['./caad.component.css']
})
export class CaadComponent implements OnInit {
  activeCustomer:any = {}
  is_metered:boolean = false;
  lineItems;
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
  caadAccountType;
  caadAccountNo;
  vats:any = [{name:2.5},{name:5.5},{name:7.5}]
  constructor(private sharedService:SharedService, 
    private customerCaadService:CustomerCaadService,
    private store :Store, private customerService: CustomerService,
    private route: ActivatedRoute,private notificationService: NotificationService) {
    if(this.is_metered){
      this.lineItems = [] as IMeteredCaadLineItem[];
    }
    else{
      this.lineItems = [] as IUNMeteredCaadLineItem[];
    }
   }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
        this.customerService.fetchSinglecustomer(params).subscribe((response)=>{
          console.log(response)
          if (response.status){
            this.customer = response.data[0]
          }
          else{alert(response.message)}
        })
    
    });
    
  }

  ngAfterViewInit(){
    const sel:any = document.querySelector('#accounttype-select')
    this.caadAccountType = sel.value
  }

  chooseAccounttype($event){
    this.caadAccountType = $event.target.value
  }

  loadCustomer($event){
    const accNo:any = document.querySelector("#caad-accountno")
    this.caadAccountNo = accNo.value
    if(this.caadAccountNo.length < 1 || this.caadAccountNo == ''){
      this.customer={};
      return this.notificationService.error("No account number was specified",'Failure',{})
    }
    const params = {accounttype:this.caadAccountType.toLowerCase(),accountno:this.caadAccountNo}
    console.log(params)
    this.customerService.fetchSinglecustomer(params).subscribe((response)=>{
      console.log(response)
      if (response.status){
        console.log(response.data)
        this.customer = response.data[0]
        this.notificationService.success('Customer has been bound to this caad request','Success',{})
      }
      else{this.customer={};this.notificationService.error(response.message,'Failure',{})}
    })
    
  }

  /* Method to check if the previous lineitem is completed before adding a new lineitem */
  isPreviousMabFilled(){
    console.log(this.lineItems[this.lineItems.length-1])
    return this.lineItems[this.lineItems.length-1]?.mab == undefined
  }

  trackByFn(index: number, item: any) {
    return item.index; 
  }

  selectVatOption($event){
    this.selectedVat = parseFloat($event.target.value)
  }

  calculateRefund(){
    this.refundAmountRaw = this.totalEstimate - this.tebmRaw
    this.refundAmount = `NGN ${this.refundAmountRaw.toLocaleString('en-US') || 0.00}`
  }

  addCaadLineItem($event){
    if(this.lineItems.length > 0){
      if(this.isPreviousMabFilled()){
        return alert("You must complete the previous lineitem before proceeding")
      }
    }
    const index = this.lineItems.length + 1
    const uuid = this.sharedService.generateUUIDStr()
    if(this.is_metered){
      this.typeLineItem = new MeteredCaadLineItem(index,uuid)
      if(this.lineItems.length > 0){
        this.typeLineItem.present_reading = this.lineItems[0].present_reading
        this.typeLineItem.last_actual_reading = this.lineItems[0].last_actual_reading
        this.typeLineItem.consumed = this.lineItems[0].present_reading - this.lineItems[0].last_actual_reading
      }
      
    }
    else{
      this.typeLineItem = new UnmeteredCaadLineItem(index,uuid)
    }
    this.lineItems.push(this.typeLineItem)
    this.isPreviousMabFilled()
  }

  deleteLineItem(uuid){
    this.lineItems =  this.lineItems.filter(obj => obj.uuid !== uuid);
  }

  getMonthsDifference(index){
    let idx = index - 1
    const fromDate = new Date(this.lineItems[idx]?.from_date)
    const toDate = new Date(this.lineItems[idx]?.to_date)
    return (
        toDate.getMonth() -
        fromDate.getMonth() +
        12 * (toDate.getFullYear() - fromDate.getFullYear())
      );
  }

  enableToDate($event,index){
    const toDate:any = document.querySelector(`#to_${index}`)
    toDate.removeAttribute("disabled")
  }

  lineItemHandler($event,index){
    const monthsDifference = this.getMonthsDifference(index)
        if (monthsDifference == 0){
            return alert("You have selected dates less than a month...")
        }
    this.lineItems[index-1].months = monthsDifference

    if(isNaN(monthsDifference)){
    }
    else{this.tarrifSelected(monthsDifference)}

        if(isNaN(this.lineItems[index-1].tarrif)){
        }
        else{
            if (document.getElementById('is_metered').getAttribute('value') != '1'){
                this.recomUnits(this.lineItems[index-1].tarrif,index-1)
            }
        }
    
  }

  tarrifSelected(index){
    let idx = index - 1  
    if (this.lineItems[idx].from_date != null && this.lineItems[idx].to_date != null && Number.isInteger(this.lineItems[idx].months)){
    }

    if (!this.is_metered){
        if(isNaN(this.lineItems[idx].tarrif)){

        }
        else{this.recomUnits(this.lineItems[idx].tarrif,idx)}
        this.getEbmSummation()
    }
    
    else if (this.is_metered){
        if(isNaN(this.lineItems[idx].tarrif) || isNaN(this.lineItems[idx].present_reading)){
            console.log(this.lineItems[idx].tarrif, this.lineItems[idx].present_reading)
        }
        else{this.recomUnits(this.lineItems[idx].consumed,idx)}
    }
  }

  recomUnits(value,idx){
    if (!this.is_metered){
        const mab = this.lineItems[idx].recom_unit * this.lineItems[idx].tarrif
        this.lineItems[idx].mab = mab
        const ebm = this.lineItems[idx].months * mab
        this.lineItems[idx].ebm = ebm
        this.getEbmSummation()
        this.calculateRefund()
    }
    else if (this.is_metered){
        this.calculateAverageUnits(idx)
    }
  }

  calculateAverageUnits(idx){
  var consumedList:any = []
  if (this.lineItems[idx].present_reading != null && this.lineItems[idx].present_reading != null){
      if (this.lineItems[idx].present_reading >= this.lineItems[idx].last_actual_reading){
          var consumed = this.lineItems[idx].present_reading - this.lineItems[idx].last_actual_reading
          this.lineItems[idx].consumed = consumed
          
          const monthsSum = this.lineItems.reduce((acc, obj) => acc + (obj.months || 0), 0);
          for (let lineItem of this.lineItems){
            consumedList.push(lineItem.consumed)
        }
          consumedList = new Set(consumedList) // with initial value to avoid when the array is empty
          consumedList = Array.from(consumedList)
          console.log("consumed list ",consumedList, "months sum ", monthsSum)
          if(consumedList.length > 1){return alert("Error in Varying consumed units")}

          let averageConsumedUnits = consumedList[0]/monthsSum //parseInt(document.getElementById('caad_line_items_table_last').getAttribute('value'))
          for (let lineItem of this.lineItems){//Recompute here
            lineItem.recom_unit = averageConsumedUnits
            let monthsDifference = lineItem.months
            const actualBilling = monthsDifference * (lineItem.tarrif * lineItem.recom_unit )
            lineItem.mab = actualBilling
            lineItem.ebm = actualBilling
          }
         
          this.getEbmSummation()
          this.calculateRefund()
      }

      else {return console.log("Last actual reading cannot be more than present reading")}
  }
  else{}

  }

  getEbmSummation(){
    const sebmRaw = this.lineItems.reduce((acc, obj) => acc + (obj.ebm || 0), 0);
    this.sebm = `NGN ${sebmRaw.toLocaleString('en-US')}`
    const tax = (parseFloat(this.selectedVat)/100) + 1
    this.tebmRaw = sebmRaw * tax
    this.tebm = `NGN ${this.tebmRaw.toLocaleString('en-US')}`
  }

  getCaadHeaders(){
    console.log("Headers region ",this.customer,  this.customer.region, this.customer.servicecenter)
    if (this.customer.account_no == undefined){
      return alert('No customer was loaded')
    }
    let headersObject:any = {}
    headersObject.region =  this.customer.region
    headersObject.state =  this.customer.state
    headersObject.servicecenter =  this.customer.servicecenter
    headersObject.buid =  this.customer.buid
    if (headersObject.state == '' || headersObject.buid=='' || headersObject.servicecenter == ''){alert("Missing Location Information Ensure this customer has a State, Business Hub & Servicenter");return false}
    headersObject.account_no = this.customer.accountno
    headersObject.buid_code =  this.customer.bucode
    headersObject.vat = this.selectedVat
    headersObject.is_metered = this.is_metered
    headersObject.refund_amount = this.refundAmountRaw
    headersObject.total_accrued = this.tebmRaw
    headersObject.current_outstanding_bal = 0.00
    headersObject.total_estimate = this.totalEstimate
    headersObject.customer_name = this.customer.firstname + " " + this.customer.surname + " " + this.customer.othernames
    return headersObject
  }

  submit(){
    console.log('Total Estimate ', this.totalEstimate)
    console.log('Selected Vat ', this.selectedVat)
    console.log("LineItems ",this.lineItems)
    const payload = {header:this.getCaadHeaders(),line_items:this.lineItems}
    console.log(payload)
    this.store.dispatch(new CreateCaad(payload))

  }

  exit($event){
    document.getElementById('caad_creation').classList.remove("content-active")
  }

}


