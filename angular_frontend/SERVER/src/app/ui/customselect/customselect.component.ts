import { UserService } from 'src/app/services/user.service';
import { Component, EventEmitter, Input, Output, OnDestroy  } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/basestore/app.states';
import { FetchBusinessHubs, FetchServiceCenters } from './state/customselect.actions';
import { getLocationsState, getServiceCenters } from './state/customselect.selector';

@Component({
  selector: 'app-custom-select',
  templateUrl: './customselect.component.html',
  styleUrls: ['./customselect.component.css']
})

export class CustomselectComponent {
  @Input() options: any[];
  @Input() updatetitle: any;
  @Input() defaultTitle: string;
  @Input() selectedOption: any;
  @Input() type: any;
  @Input() model: any;
  @Output() selectionChange = new EventEmitter<any>();
  title = "Select User Creation Priviledge";
  value=""
  
  constructor() {

  }

  ngOnInit(): void {
    console.log(this.updatetitle)
    this.defaultTitle = this.updatetitle = this.title
    let dropdown = document.getElementById('app-user-positions-update')
    console.log(dropdown)
      if(dropdown != null){
        dropdown.querySelector('a').textContent = this.updatetitle
      }
  }

  setTitle(title){
    this.title = title
  }

  onSelect(option: any) {
      this.selectedOption = option;
      this.title = this.selectedOption?.name || this.selectedOption
      this.value = this.selectedOption.code || this.selectedOption
      this.selectionChange.emit(this.selectedOption);
  }


  ngOnDestroy(){}
   
}

