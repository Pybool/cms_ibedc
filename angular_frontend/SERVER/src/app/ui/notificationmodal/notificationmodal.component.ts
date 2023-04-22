import { ChangeDetectorRef, Component } from '@angular/core';
import { take } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification.service';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';

@AutoUnsubscribe
@Component({
  selector: 'app-notificationmodal',
  templateUrl: './notificationmodal.component.html',
  styleUrls: ['./notificationmodal.component.css']
})
export class NotificationmodalComponent {
  type = 'failure'
  title = 'CAAD Approval Success'
  message = 'This action completed successfully and an email has been sent to the Regional head'
  subMessage = 'Please await further approvals'
  msgIsArray = false;
  kycerrors = []

  constructor(private notificationService: NotificationService,private changeDetectorRef: ChangeDetectorRef){
    this.notificationService.getActiveNotification().subscribe((notification)=>{
      this.type = notification.type
      this.title = notification.title
      this.message = notification.message
      this.subMessage = notification.subMessage
      console.log(notification)
      if(Array.isArray(this.message)){
        this.msgIsArray = true
        this.kycerrors = this.message
      }
      else{

      }
    })
  }

  ngAfterViewInit(){
    console.log("Resizing viewport")
  }

  closeModal($event){
    this.resetModal()
}


  resetModal(){
    this.type = null
    this.title = null
    this.message = null
    this.subMessage = null
  }

  showModal(type,tab){
    if (type=='success'){
        var modal = document.getElementById('modalAlert')
        var title = document.getElementById('success-title')
        var msg = document.getElementById('success-msg')
        var subMsg = document.getElementById('success-sub-msg')
        title.innerHTML = `Success!!, ${tab} draft was saved`
        msg.innerHTML = `You’ve successfully saved ${tab} draft `
        subMsg.innerHTML = `You can re-edit this information by selecting the customer again in the drafts list tab.`
        modal.classList.add('show')
        modal.style.display = 'block'
        this.changeDetectorRef.detectChanges();
        // modal.setAttribute('aria-hidden',false)

    }
    else{
        var modal = document.getElementById('fail-modalAlert')
        var title = document.getElementById('fail-title')
        var msg = document.getElementById('fail-msg')
        var subMsg = document.getElementById('fail-sub-msg')
        title.innerHTML = `Failed, ${tab} draft was not saved!`
        msg.innerHTML = `${tab} draft could not be saved at this time, please try later `
        subMsg.innerHTML = `This operation failed`
        modal.classList.add('show')
        modal.style.display = 'block'
        this.changeDetectorRef.detectChanges();
        // modal.setAttribute('aria-hidden',false)
    }
}
}
