import { Component } from '@angular/core';
import { ConfigurationsService } from 'src/app/services/configurations.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-usersettings',
  templateUrl: './usersettings.component.html',
  styleUrls: ['./usersettings.component.css']
})
export class UsersettingsComponent {
  public user_positions:any;
  cust_cu_roles;
  cust_kyc_roles;
  biz_hub_ops_roles;
  caad_roles;
  user_position_codes;

  constructor(private userService : UserService, private configurationService:ConfigurationsService){}

  ngOnInit(){
    this.userService.fetchMetadata().subscribe((data)=>{
      this.user_positions = data.positions
      console.log(this.user_positions)
    })

    this.configurationService.getUserSettingsMetaData().subscribe((metaData)=>{
      console.log("Metadat from service ====> ", metaData)
      this.cust_cu_roles = metaData.cust_cu_roles
      this.cust_kyc_roles = metaData.cust_kyc_roles
      this.biz_hub_ops_roles = metaData.biz_hub_ops_roles
      this.caad_roles = metaData.caad_roles
      this.user_position_codes = metaData.user_position_codes
    })
  }

  submit($event){
    const positionCodesInput:any = document.getElementById('position-codes-input')
    const positionCode = positionCodesInput.value?.toUpperCase().replace(/\s/g, "");
    this.configurationService.createPositionCode({name:positionCode}).subscribe((response)=>{
      alert(response?.message)
    })
  }

  private deleteByKey(array, keyToDelete) {
    return array.filter(item => item.id !== keyToDelete);
  }
  

  deletePill($event){
    this.configurationService.deletePositionCode($event.target.id).subscribe((response)=>{
      if(response.status){
        const newArr = this.deleteByKey(this.user_position_codes,parseInt($event.target.id))
        console.log(newArr)
        this.user_position_codes = newArr
      }
      alert(response?.message)
    })
  }
}
