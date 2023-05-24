import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CustomervalidationService {
  String:any;
  constructor() { }
    
   public check_kyc_compliance(data=[], mode = 'edit') {
    let error_list = [];
    console.log(data)
    const validate_a_z_string = (value) => /[A-Za-z]/.test(value) && value?.length >= 1;
    const validate_a_z_num_string = (value) => /[A-Za-z]{2,25}\s[A-Za-z]{2,25}/.test(value) && value?.length >= 3;
    const validate_not_empty = (value) => value?.length > 1;
    const validate_no_number_in_string = (value) => !/\d/.test(value);
    const validate_not_null_none = (value) => value != null && value != undefined && value != '';
  
    const validate_account_number = (value) => validate_not_empty(value) && validate_not_null_none(value) && value?.length >= 5;
    const validate_surname = (value) => validate_a_z_string(value) && validate_not_empty(value) && validate_not_null_none(value) && validate_no_number_in_string(value);
    const validate_firstname = (value) => validate_a_z_string(value) && validate_not_empty(value) && validate_not_null_none(value) && validate_no_number_in_string(value);
    const validate_othernames = (value) => validate_a_z_string(value) && validate_not_empty(value) && validate_not_null_none(value) && validate_no_number_in_string(value);
    const validate_phone = (value) => !isNaN(Number(value)) && value?.length >= 10 && value?.length <= 11;
    const validate_states = (value) => ['Oyo', 'Ogun', 'Osun', 'Kwara', 'Niger', 'Ekiti', 'Kogi','Ibadan'].includes(value?.toProperCase()) && validate_a_z_string(value);
    const validate_city = (value) => validate_a_z_string(value) && validate_not_null_none(value) && validate_no_number_in_string(value);
    const validate_address = (value) => validate_not_null_none(value) && value?.length >= 0;
    const validate_dss_id = (value) => validate_not_null_none(value);
    const validate_status_code = (value) => validate_not_null_none(value) && value?.length != 0 && validate_no_number_in_string(value)  && ['A','P','S','I'].includes(value)
    const validate_email = (value) => /^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$/.test(value);
    const validate_accounttype = (value) => ['Prepaid', 'Postpaid'].includes(value?.toProperCase()) && validate_a_z_string(value);
    const validate_gender = (value) => ['Male', 'Female'].includes(value?.toProperCase()) && validate_a_z_string(value);
  
    const check_compliance = () => {
   
      const [ account_number, accounttype, gender, surname, firstname, othernames, phone, state, region,buid, servicecenter, city, address, address1, dss_id, feederid, status_code, email ] = data || ['9000000','Prepaid', 'Male', 'Eko1011','Emmanuel','','08100000000','Edo','Oyo', 'Molete', 'Apata', 'Ibadan','Molete','ACE884734834839989430','A','eko@gmail.com'];
      if(mode=='edit'){if (!validate_account_number(account_number)) error_list.push('Account number field must not be empty and must be at least 5 characters long!: [Accounts Information Tab]');    }
      if (!validate_accounttype(accounttype)) error_list.push('Account Type must be either Prepaid or Postpaid');
      if (!validate_gender(gender)) error_list.push('Gender must be either Male or Female');
      if (!validate_surname(surname)) error_list.push('Surname field must not be empty and must be a string without numbers');
      if (!validate_firstname(firstname)) error_list.push('Firstname field must not be empty and must be a string without numbers');
      if (!validate_othernames(othernames)) error_list.push('Other names must not be empty and must be a string without numbers');
      if (!validate_phone(phone)) error_list.push('Mobile field must not be empty and must be a 11 digits long containing only numbers');
      if (!validate_states(state)) error_list.push('State field must not be empty and must be a valid state supplied by IBEDC');
      if (!validate_states(region)) error_list.push('Region field must not be empty and must be a valid state supplied by IBEDC');
      if (!validate_dss_id(buid)) error_list.push('Business Unit field must not be empty');
      if (!validate_dss_id(servicecenter)) error_list.push('Service Center field must not be empty');
      if (!validate_city(city)) error_list.push('City field must not be empty and must be a string without numbers');
      if (!validate_address(address) && !validate_address(address1)) error_list.push('Address field must not be empty');
      if (!validate_dss_id(dss_id)) error_list.push('Dss Name field must not be empty');
      if (!validate_dss_id(feederid)) error_list.push('Feeder Name field must not be empty');
      if (!validate_status_code(status_code)) error_list.push('Status Code field must not be empty and must either A, P, S, I');
      if (!validate_email(email)) error_list.push('Invalid email entered');
      
      if(error_list.length == 0){
        return []
      }
      return error_list;
    }
    
    return check_compliance();
  }
  

}
          



