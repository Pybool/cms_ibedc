import { Component, Input } from '@angular/core';
import { SharedService } from 'src/app/services/shared.service';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';

@AutoUnsubscribe
@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.css']
})
export class SpinnerComponent {
  @Input() text: string = 'Loading...';

  constructor(private sharedService: SharedService){
    this.sharedService.getSpinnerText().subscribe((text)=>{
      this.text = text
    })

  }

}
