import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { data } from 'jquery';
import { UserState } from 'src/app/authentication/state/auth.selector';
import { AppState } from 'src/app/basestore/app.states';
import { CustomerService } from 'src/app/services/customer.service';
import { CustomercreationupdateService } from 'src/app/services/customercreationupdate.service';
import { CustomervalidationService } from 'src/app/services/customervalidation.service';
import { NotificationService } from 'src/app/services/notification.service';
import { SharedService } from 'src/app/services/shared.service';
import { ecmiCustomers, emsCustomers } from '../customersmodule/prepaidcustomers/state/customer.selector';
import { NewCustomer, LoadCustomer } from './customercreation.model';
import * as helper from './scripts'
import { FetchDrafts, LoadDraft, SaveDraft } from './state/customercreation.actions';
import { fetchedDrafts, loadedDraft } from './state/customercreation.selector';

interface CustomWindow extends Window {
  DataTable: (searchTerm: string,{}) => void;
}

declare let window: CustomWindow;
// Helper function to set dropdown value

@Component({
  selector: 'app-customercreation',
  templateUrl: './customercreation.component.html',
  styleUrls: ['./customercreation.component.css']
})
export class CustomercreationComponent implements OnInit {
  newCustomer = new NewCustomer()
  formHeader:string = 'Create Customer'
  locationType;
  locations;
  userState;
  permission_hierarchy;
  accounttypes;
  building_descriptions;
  customer_categorys;
  customer_types;
  premise_types;
  supply_types;
  service_bands;
  userFetched = false;
  service_centers;
  business_units;
  user_region;
  user_buid;
  user_servicecenter;
  loadedDraftIsNew = true;
  draft_id = 0;
  draftTag = null;
  drafts;
  loadedDraft;
  loadedDraft$;
  fetchedDraftsList;
  customersList$;
  currentAccountno;
  emailExistsRows;
  mobileExistsRows;
  accountnoExistsRows;
  draftFields = {basic_information:['title','surname','firstname','othernames','gender','email','mobile'],
                account_information:['accountno','accounttype','customer_type','business_type','statuscode','cin'],
                location_information:['building_description','premise_type','address','address1','lga','region','buid','servicecenter','city','state'],
                asset_information:['dss_id','feederid','service_band','injection_sub_station','meteroem','ltpoleid','dss_name','dss_owner','feeder_type','feeder_name',],
                landlord_information:['landlord_name','landlord_phone']}

  constructor(private store: Store<AppState>,
              private customerService: CustomerService,
              private sharedService: SharedService,private notificationService: NotificationService,
              private customerCreateUpdateService:CustomercreationupdateService,
              private customervalidationService: CustomervalidationService
              ) { 
    this.userState = this.store.select(UserState);
    this.customerService.fecthCustomerFormMetadata().subscribe((data)=>{
      console.log(data)
      this.locationType = data.locations.type
      this.locations = data.locations[this.locationType]
      this.accounttypes = data.options_object_dict.accounttype
      this.building_descriptions = data.options_object_dict.building_description
      this.customer_categorys = data.options_object_dict.customer_category
      this.customer_types = data.options_object_dict.customer_type
      this.premise_types = data.options_object_dict.premises_type
      this.supply_types = data.options_object_dict.supply_type
      this.service_bands = data.options_object_dict.service_band
    })
  }

  ngOnInit(): void {
    this.userState.subscribe((user) => {
      if (user == undefined){}
      else{

        this.permission_hierarchy = user?.permission_hierarchy.replaceAll(" ","_").toLowerCase()
        this.user_region = user.region
        this.user_buid = user.business_unit 
        this.user_servicecenter = user.service_center   
        console.log(user)
        console.log(user.region, user.business_unit, user.service_center, user.permission_hierarchy)  
      }
    });

    this.customerCreateUpdateService.getDraftId().subscribe((id)=>{
      this.draft_id = id
    })

    this.sharedService.getFormHeader().subscribe((arr)=>{
      console.log(arr)
      this.formHeader = arr[1]
      if(arr[0] == 'edit'){
        this.currentAccountno = arr[3]
        this.customerService.fetchSinglecustomer({accounttype:arr[2],accountno:this.currentAccountno}).subscribe((state) => {
          console.log("[Single customer ]====> ",state)
          this.loadCustomer(state.data[0] || state.data)
        });

      }
    })
  }

  getGisAssetdata(asset_type){
    console.log(asset_type)
    helper.getGisAssetdata(asset_type)
  }

  saveDraft($event,type){
    if (this.draftTag == null){
      let tag = prompt("Please enter a tag for this draft")

      if (tag != null && tag != "") {
        this.sharedService.generateUUID().subscribe((uuid)=>{
          this.draftTag = String(tag) + '##'+ String(uuid)
        })
        console.log(this.draftTag)
      }
      else{return alert("Invalid or no tag name was supplied")}
    }
    
    let customer = Object.assign({}, this.newCustomer);
    let dss_id:any = document.getElementById('dss_id')
    let dss_owner:any = document.getElementById('dss_owner')
    let feederid:any = document.getElementById('feederid')
    let feeder_type:any = document.getElementById('feeder_type')
    customer.dss_id = dss_id.value
    customer.dss_name = dss_id.textContent
    customer.feederid = feederid.value
    customer.feeder_type = feeder_type.textContent
    customer.dss_owner = dss_owner.textContent
    customer.feeder_name = feederid.textContent
    let draft = {}

    for (let field of this.draftFields[type]){
      if(field != 'buid' && field !='servicecenter' && field !='region'){
        draft[field] = customer[field] || ''
      }
      else{
        switch(field){
          case 'region':
            draft[field] = customer[field] || this.user_region
            break;
          case 'buid':
            draft[field] = customer[field] || this.user_buid
            break;
          case 'servicecenter':
            draft[field] = customer[field] || this.user_servicecenter
            break;
          default:
            break;
        }
      }
    }
    console.log(`${type}`,draft)
    let payload = {type:type,draft:draft,is_new:this.loadedDraftIsNew,draft_id:this.draft_id,draft_tag:this.draftTag}
    this.store.dispatch(new SaveDraft(payload))
  }

  fetchDrafts(){
    this.store.dispatch(new FetchDrafts())
    this.fetchedDraftsList = this.store.select(fetchedDrafts);
    this.fetchedDraftsList.subscribe((state) => {
      this.drafts = state.drafts
    });
  }

  loadDraft($event){
    this.store.dispatch(new LoadDraft({tag:$event.target.id,drafts:this.drafts}))
    let dataToLoad = {}
    let flattenedFields = Object.values(this.draftFields).flat();
    this.loadedDraft$ = this.store.select(loadedDraft).subscribe((state) => {
      this.loadedDraft = state.draft
      console.log(state.draft)
      for(let field of flattenedFields){
        dataToLoad[field] = this.loadedDraft[field]
      }
      this.newCustomer = new LoadCustomer(dataToLoad)
      this.draftTag = state.draft.draft_tag
      
      
      
    });
    this.setAssetsDropdowns()
    this.loadedDraft$.unsubscribe()


    /* If Regional User, service centers  */
    if(this.permission_hierarchy == 'region'){
      this.customerService.fetchLocations('servicecenter',this.newCustomer.buid).subscribe((data)=>{
        this.service_centers = data.data.service_centers
      })
    }
    /* If Head Quarters User, get business uints and corresponding service centers  */
    else if(this.permission_hierarchy == 'hq'){
      this.customerService.fetchLocations('business_unit',this.newCustomer.region).subscribe((data)=>{
        this.business_units = data.data.service_centers
      })
      this.customerService.fetchLocations('servicecenter',this.newCustomer.buid).subscribe((data)=>{
        this.service_centers = data.data.service_centers
      })
    }
  }

  loadCustomer(data){
    // if(data.accounttype == 'Prepaid'){
    //   this.draftFields.account_information.push('address')
    // }
    // else if (data.accounttype == 'Postpaid'){
    //   this.draftFields.account_information.push('address1')
    // }
    let dataToLoad = {}
    let flattenedFields = Object.values(this.draftFields).flat();
      for(let field of flattenedFields){
        dataToLoad[field] = data[field]
      }
      this.newCustomer = new LoadCustomer(dataToLoad) 
      this.setAssetsDropdowns()   
      console.log("Loaded ====> ", this.newCustomer)  

  }

  fetchServiceCenters($event){
    this.customerService.fetchLocations('servicecenter',$event.target.value).subscribe((data)=>{
      this.service_centers = data.data.service_centers
    })
  }

  fetchBusinessUnits($event){
    this.customerService.fetchLocations('business_unit',$event.target.value).subscribe((data)=>{
      this.business_units = data.data.business_units
      this.service_centers = []
      this.userFetched = true
    })
  }

  submit(){
    console.log("Customer data =====> ",this.newCustomer)
    let buffer = new Array()

    const mandatoryField =  [ 'accountno', 'accounttype', 'gender', 'surname', 'firstname', 'othernames', 'mobile', 'state', 'region','buid', 'servicecenter', 'city','address', 'address1', 'dss_id', 'feederid', 'statuscode', 'email' ] 
    mandatoryField.forEach((field)=>{
      buffer.push(this.newCustomer[field])
    })
    let status = this.customervalidationService.check_kyc_compliance(buffer,'create')
    if(status == true){
      console.log("Submitting awaiting customer ")
      this.customerCreateUpdateService.checkOrCreateNewAwaitingCustomer(this.newCustomer).subscribe((response)=>{
        console.log("[SERVER::::::>] ", response)
        if(response.exists){
          this.emailExistsRows = response.data.email_exists
          this.mobileExistsRows = response.data.mobile_exists
          this.accountnoExistsRows = response.data.accountno_exists
          return this.existspopupModal("Found records sharing some key fields!",response.message,response.data)
        }
        if(response.status == true && response.exists == false){
          //Load Notification Modal here....
          let notification = {type:'success',title:'Awaiting Customer Created',
          message:response?.message,
          subMessage:'A mail has been sent to the approving officer'}
          this.notificationService.setModalNotification(notification)
        }
        else{
          //Load Notification Modal here....
          let notification = {type:'failure',title:'Something went wrong',
          message:response?.message,
          subMessage:'Awaiting Customer failed'}
          this.notificationService.setModalNotification(notification)
        }
      })
    }
    return console.log(status)
  }

  createUpdateAwaitingCustomer($event,create=false){
    
    if(create == false){
      console.log("Awaiting customer to update ---> ", $event.target.closest('tr')?.id)
      const rowid = parseInt($event.target.closest('tr')?.id)
      let action = confirm("Are you sure you want to update this record in the queue? \n\n Updating a record in this manner will not update the account number of this customer")
      if (action){
          if(this.newCustomer != undefined){
            this.newCustomer['force'] = false
            const payload = {rowid:rowid,data:this.newCustomer}
            this.customerCreateUpdateService.updateExistsAwaitingCustomer(payload).subscribe((response)=>{

            })
          }
      }
      return
    }
    this.newCustomer['force'] = true
    const payload = {rowid:0,data:this.newCustomer}
    this.customerCreateUpdateService.createExistsAwaitingCustomer(payload).subscribe((response)=>{
        
    })        
   
  }

  private existspopupModal(headertitle, message, data) {
    const modal:any = document.getElementById('exists-modalAlert');
    const title:any = document.getElementById('exists-title');
    const msg:any = document.getElementById('exists-msg');
    title.textContent = headertitle;
    msg.textContent = message;
    ['email', 'mobile', 'accountno'].forEach((id, i) => {
      // const table = document.querySelector(`#${id}-exists-table`);
      // table.innerHTML = '';
    console.log(window.DataTable)
    setTimeout(()=>{
      new window.DataTable(`#${id}-exists-table`, {
        "pageLength": 50,
        "bPaginate": true,
        "responsive": true,
        "processing": true,
        "searching": false,
        "bdeferRender": true,
      });
    },5000)
      
    });
    alert(message)
    modal.classList.add('show');
    modal.style.display = 'block';
    modal.setAttribute('aria-hidden', false);
  }

  private setAssetsDropdowns(){
    let dss_id:any = document.getElementById('dss_id')
    let dss_owner:any = document.getElementById('dss_owner')
    let feederid:any = document.getElementById('feederid')
    let feeder_type:any = document.getElementById('feeder_type')
    dss_id.value = this.newCustomer?.dss_id;
    dss_id.textContent = this.newCustomer?.dss_name;
    feederid.value = this.newCustomer?.feederid
    feeder_type.textContent = this.newCustomer?.feeder_type
    dss_owner.textContent = this.newCustomer?.dss_owner
    feederid.textContent = this.newCustomer?.feeder_name
    
  }

  closeSlideModal(){
    document.getElementById('create_customer').classList.remove("content-active")
  }

  ngOnDestroy(){
    this.loadedDraft$?.unsubscribe()
    this.customersList$?.unsubscribe()
  }

}


