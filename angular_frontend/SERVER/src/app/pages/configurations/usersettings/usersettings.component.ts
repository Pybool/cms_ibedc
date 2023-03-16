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
  caad_roles

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
    })
  }
}
