
export class CreateUser {
    name: string;
    email: string;
    password?: string;
    position?: string;
    privilege?: string;
    can_create_customers?: boolean;
    can_create_user?:boolean;
    can_approve?: boolean;
    can_approve_caad?: boolean;
    can_manage_2fa?: boolean;
    permission_hierarchy?:boolean;
    hq_radio?:string;
    region_radio?:string;
    bizhub_radio?:string;
    service_center_radio?:string;
    groups?: string[];
    enable_2fa?: boolean;
    region?: string;
    business_unit?: string;
    service_center?: string;

    public clone(): CreateUser {
      return new CreateUser();
  }
  }
  
  export class UpdateUser {
    update_name: string;
    update_email: string;
    update_password?: string;
    update_position?: string;
    update_privilege?: string;
    update_can_create_customers?: boolean;
    update_can_create_user?:boolean;
    update_can_approve?: boolean;
    update_can_approve_caad?: boolean;
    update_can_manage_2fa?: boolean;
    update_permission_hierarchy?:boolean;
    update_groups?: string[];
    update_enable_2fa?: boolean;
    update_region?: string;
    update_business_unit?: string;
    update_service_center?: string;
  }


  export class UserFilters{
    position:string;
    can_create_customers:boolean;
    can_create_user:boolean;
    can_approve:boolean;
    can_approve_caad:boolean;
    can_manage_2fa:boolean;
    permissions_hierarchy:string;
    region:string;
    business_unit:string;
    servicecenter:string;
    status:string;
    constructor(

      // public position,
      // public can_create_customers,
      // public can_create_user,
      // public can_approve,
      // public can_approve_caad,
      // public can_manage_2fa,
      // public permissions_hierarchy,
      // public region,
      // public business_unit,
      // public servicecenter,
      // public status,
   
  ){}
  }
   
export class UserModifyModel {
  update_name: string;
    update_email: string;
    update_password?: string;
    update_position?: string;
    update_privilege?: string;
    update_can_create_customers?: boolean;
    update_can_create_user?:boolean;
    update_can_approve?: boolean;
    update_can_approve_caad?: boolean;
    update_can_manage_2fa?: boolean;
    update_permission_hierarchy?:boolean;
    update_groups?: string[];
    update_enable_2fa?: boolean;
    update_region?: string;
    update_business_unit?: string;
    update_service_center?: string;
    constructor(
        public name,
        public email,
        public password,
        public position,
        public privilege,
        public can_create_customers,
        public can_create_user,
        public can_approve,
        public can_approve_caad,
        public can_manage_2fa,
        public permissions_hierarchy,
        public groups ,
        public enable_2fa,
        public region,
        public business_unit,
        public servicecenter,
     
    ) {
        this.name = name
        this.email = email
        this.password = password
        this.position = position
        this.privilege = privilege
        this.can_create_customers = can_create_customers
        this.can_create_user = can_create_user
        this.can_approve = can_approve
        this.can_approve_caad = can_approve_caad
        this.can_manage_2fa = can_manage_2fa
        this.permissions_hierarchy = permissions_hierarchy
        this.groups = groups
        this.enable_2fa = enable_2fa
        this.region = region
        this.business_unit = business_unit
        this.servicecenter = servicecenter
    }
  
  }
  