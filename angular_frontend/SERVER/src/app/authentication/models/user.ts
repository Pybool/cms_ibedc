export class User {
  token?: string;
  action_id?: string;
  active?: boolean;
  avatar?: string;
  bio?: string;
  bucode?: string;
  business_unit?: string;
  can_approve?: boolean;
  can_approve_caad?: boolean;
  can_create_user?: boolean;
  can_create_customer?: boolean;
  created_at?: string;
  email: string;
  enable_2fa?: boolean;
  firstname?: string;
  id?: string;
  ig_handle?: string;
  is_regularuser?: boolean;
  is_superuser?: boolean;
  is_verified_account?: boolean;
  last_login?: string;
  lastname?: string;
  manage_2fa?: boolean;
  otp?: string;
  otp_expires_at?: string;
  permission_hierarchy?: string;
  phone1?: string;
  password?: string;
  position?: string;
  region?: string;
  secret_code_2fa?: string;
  servicecenter?: string;
  slug?: string;
  suspend_user?: boolean;
  twitter_handle?: string;
  updated_at?: string;
  user_type?: string;
  username?: string;
}
  
export class UserModel {
  constructor(
    public email: string,
    public token?: string,
    public action_id?: string,
    public active?: boolean,
    public avatar?: string,
    public bio?: string,
    public bucode?: string,
    public business_unit?: string,
    public can_approve?: boolean,
    public can_approve_caad?: boolean,
    public can_create_user?: boolean,
    public can_create_customer?: boolean,
    public created_at?: string,
    public enable_2fa?: boolean,
    public firstname?: string,
    public id?: string,
    public ig_handle?: string,
    public is_regularuser?: boolean,
    public is_superuser?: boolean,
    public is_verified_account?: boolean,
    public last_login?: string,
    public lastname?: string,
    public manage_2fa?: boolean,
    public otp?: string,
    public otp_expires_at?: string,
    public permission_hierarchy?: string,
    public phone1?: string,
    public password?: string,
    public position?: string,
    public region?: string,
    public secret_code_2fa?: string,
    public servicecenter?: string,
    public slug?: string,
    public suspend_user?: boolean,
    public twitter_handle?: string,
    public updated_at?: string,
    public user_type?: string,
    public username?: string,
  ) {}

   userToken() {
    return this.token;
  }
  
  getUser(){
    return this
  }
}
