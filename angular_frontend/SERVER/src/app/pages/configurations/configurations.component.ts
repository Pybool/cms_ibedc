import { Component, OnInit, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { take } from 'rxjs/operators';
import { ConfigurationsService } from 'src/app/services/configurations.service';
import * as helper from './scripts'

interface CustomWindow extends Window {
  positionCodes: []
}

declare let window: CustomWindow;
// Helper function to set dropdown value

@Component({
  selector: 'app-configurations',
  templateUrl: './configurations.component.html',
  styleUrls: ['./configurations.component.css']
})
export class ConfigurationsComponent implements OnInit,  OnDestroy {
  paths:string[] = ["accounttype","building_description","customer_category","customer_type","premise_type","supply_type","service_band"]
  processes;
  metaData$:any = new BehaviorSubject<any>({});
  position_codes;
  constructor(private configurationsService: ConfigurationsService) { }

  ngOnInit(): void {

    this.configurationsService.getConfigData().subscribe((data)=>{
      this.processes = data.processes
    })

    this.configurationsService.getPositionCodes().pipe(take(1)).subscribe((response)=>{
      this.position_codes = response.data
      const codes:any = []
      this.position_codes.forEach((code)=>{
        codes.push(code.name)
      })
      window.positionCodes = codes
    })
  }

  modalclose(){
    helper.modalclose()
  }

  

  saveOptions($event){
    const self = $event.target
    let data = []
    let value = self.getAttribute('value')
    let option_item_nodes:any = document.getElementsByClassName('option-item-add')
    console.log('option_item_nodes ==> ',option_item_nodes)
    if(option_item_nodes.length > 0){
      for (let option_item of option_item_nodes){
        data.push(option_item.getAttribute('value'))
    }
    }
    else{
      let pc:any = document.getElementById("position_code")
      let pn:any =  document.getElementById("newTag")
      let positionName = pc.value
      let positionCode =pn.value
      
      data = [`${positionCode} (${positionName})`,]
    }

    let precedence:any = document.getElementById('precedence')
    precedence = precedence.value;
    let process_code:any = document.getElementById('sel_position_code')
    process_code = process_code.value;

    if (this.paths.includes(value.split('_new')[0]) == false){
        if (precedence !== '-1' && process_code !== '0'){
            data.push({precedence:precedence,process_code:process_code})
        }
        else{
          if(!value.includes('edit')){
            console.log("Precedence code must be greater than 0")
          }
        }
    }
    
    if (value.includes('_new')){
      let type;
        if (data.length > 0){
          if(value.split('_new')[0] == 'user_positions'){
            let positionCode:any = document.getElementById('position_code')
            type = {position_code:positionCode.value,value:'user_positions'}
          }
          else{type = value.split('_new')[0]}
           
          const payload = {value:type,
                            data:data
                          }
          this.configurationsService.createConfigOption(payload).subscribe((data)=> {
                if (data.status){
                    helper.clearTagList()
                    alert(`${data.message}`)
                    document.location.reload()
                }
                else{alert(`${data.message}`)} 
            })
        
        }
        else{alert("No option is added to list...")}
        
    }
    else if (value.includes('_edit')){
      
      const tagList = helper.getTagList()
      const payload = {value:value.split('_edit')[0],
                        data:tagList
                      }
        this.configurationsService.updateConfigOption(payload).subscribe((data)=> {
          if (data.status){
            helper.clearTagList()
            alert(`${data.message}`)
            document.location.reload()
          }
          else{alert(`${data.message}`)}
        })
    }
    
  }

  ngOnDestroy(){
    window.positionCodes = []
  }
}
