import { Component, OnInit } from '@angular/core';
import { CrmdService } from 'src/app/services/crmd.service';
import { NotificationService } from 'src/app/services/notification.service';

@Component({
  selector: 'app-crmd',
  templateUrl: './crmd.component.html',
  styleUrls: ['./crmd.component.css']
})
export class CrmdComponent {
   queue;
   queuesData;
   filter;
   submitFilter
   viewMode
   createqueueForm;
   awaitingCustomers:any;
   awaitingCustomers$:any;
   loadedAwaitingCustomer:any;
   activeAccordionItem:string;
   editedFields:string[] = []
   newFieldsBasicInfo:any[] = []
   newFieldsAccountInfo:any[] = []
   newFieldsLocationInfo:any[] = []
   newFieldsAssetsInfo:any[] = []
   newFieldsLandlordInfo:any[] = []
  constructor(private crmdService:CrmdService,private notificationService: NotificationService){}

  ngOnInit(){
    const payload = {status:'pending'}
    this.awaitingCustomers$ = this.crmdService.fetchAwaitingCustomers(payload).subscribe((awaitingCustomers)=>{
      this.crmdService.cacheAwaitingCustomers(awaitingCustomers)
      this.awaitingCustomers = awaitingCustomers?.data
      console.log("Awaiting Customers ===> ", this.awaitingCustomers)
    })
  }

  resetFilter(){}

  getItemById(array, id) {
    return array.find(item => item.id == id);
  }

  viewAwaitingCustomer($event){
    const self = this
    this.loadedAwaitingCustomer = this.getItemById(this.awaitingCustomers,$event.target.closest('li')?.value)
    console.log("[LOADED AWAITING CUSTOMER]:: ",this.loadedAwaitingCustomer)
    this.editedFields = this.loadedAwaitingCustomer.last_edited_fields.fields
    document.getElementById('awaiting_customer_details').classList.add("content-active")
    const basic_info:any = document.getElementById('basic-info')
    const account_info:any = document.getElementById('account-info')
    const location_info:any = document.getElementById('location-info')
    const assets_info:any = document.getElementById('assets-info')
    const landlord_info:any = document.getElementById('landlord-info')
    console.log(basic_info)
    setTimeout(()=>{
      self.newFieldsBasicInfo =basic_info.querySelectorAll('span.up')
      self.newFieldsAccountInfo =account_info.querySelectorAll('span.up')
      self.newFieldsLocationInfo =location_info.querySelectorAll('span.up')
      self.newFieldsAssetsInfo =assets_info.querySelectorAll('span.up')
      self.newFieldsLandlordInfo =landlord_info.querySelectorAll('span.up')
      // console.log(newFieldsBasicInfo)
    },1000)
    
  }

  setActive($event){
    let clicked:any = $event.target
    let el;
    if(clicked.nodeName === "A"){
      el = clicked.querySelector('h6')
    }
    else{el=clicked}
    
    if(this.activeAccordionItem == clicked.closest('a').id){
        el.style.color = '#364a63';
        this.activeAccordionItem = ''
        return
    }
    const accordionHeads:any  = document.querySelectorAll('.accordion-head')
    accordionHeads.forEach((accordionHead)=>{
      accordionHead.querySelector('h6').style.color = '#364a63'
    })
    if (el){el.style.color = 'orange';this.activeAccordionItem = el.closest('a').id}
    else{el.querySelector('h6').style.color = 'orange';this.activeAccordionItem = el.closest('a').id}
    
  }

  ngAfterViewInit(){
    
  }

  queueAction($event,action){
    const commentsEl:any = document.querySelector('#comments')
    let comments = commentsEl?.value
    let payload = {id:this.loadedAwaitingCustomer.id,
                  accountno:this.loadedAwaitingCustomer.accountno,
                  action:action,
                  comments:comments,
                  is_draft:this.loadedAwaitingCustomer.is_draft,
                  is_fresh:this.loadedAwaitingCustomer.is_fresh,
                  customer_id:this.loadedAwaitingCustomer.customer_id}
    this.crmdService.performAwaitingCustomerAction(payload).subscribe((response)=>{
        if (response?.status){
          //Load Notification Modal here....
          let notification = {type:'success',title:'CRMD Approval Successful!',
          message:response?.message,
          subMessage:'CRMD Approval Sequence Milestone'}
          this.notificationService.setModalNotification(notification)
        }
    })
  }

  exitAwaitingCustomer(){
    document.getElementById('awaiting_customer_details').classList.remove("content-active")
  }
  

  ngOnDestroy(){
    this.awaitingCustomers$?.unsubscribe()
  }

}
