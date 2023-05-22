export class NewCustomer {
    title?: string | '';
    surname:string;
    firstname:string;
    othernames?:string;
    gender: string | null;
    email: string | null;
    mobile: string | null;
    accountno?:string;
    accounttype: string | null;
    customer_type?: string | null;
    business_type?: string | null;
    cin?: string | null;
    statuscode:string;

    building_description?: string | null;
    lga?: string | null;
    premise_type?: string | null;
    address1:string;
    address:string;
    region: string ;
    buid: string ;
    servicecenter: string ;
    city:string;
    state:string;
    feeder_type?: string | null;
    feeder_name?: string | null;
    service_band?: string | null;
    dss_id?: string | null;
    dss_name?: string | null;;
    dss_owner?: string | null;;
    meteroem?:string | null;
    landlord_name?: string | null;
    landlord_phone?: string | null;
    injection_sub_station?: string | null;
    last_edited_fields?:any;
    upriserid?: string | null;
    feederid?: string | null;
    ltpoleid?: string | null;
  }

  export class LoadCustomer {
    title;
    surname;
    firstname;
    othernames;
    gender;
    email;
    mobile;
    accountno;
    accounttype;
    customer_type;
    business_type;
    cin;
    statuscode;
    building_description;
    lga;
    premise_type;
    address1;
    address;
    region ;
    buid ;
    servicecenter ;
    city;
    state;
    feeder_type
    feeder_name;
    service_band;
    dss_id;
    dss_name;
    dss_owner;
    meteroem;
    landlord_name;
    landlord_phone;
    injection_sub_station;
    upriserid;
    feederid;
    ltpoleid;

    constructor(public customer:any){
        this.title = customer.title;
        this.surname = customer.surname;
        this.firstname = customer.firstname;
        this.othernames = customer.othernames;
        this.gender = customer.gender;
        this.email = customer.email;
        this.mobile = customer.mobile;
        this.accountno = customer.accountno;
        this.accounttype = customer.accounttype;
        this.customer_type = customer.customer_type;
        this.business_type = customer.business_type;
        this.cin = customer.cin;
        this.statuscode = customer.statuscode;
        this.building_description = customer.building_description;
        this.lga = customer.lga;
        this.premise_type = customer.premise_type;
        this.address1 = customer.address1;
        this.address = customer.address;
        this.region = customer.region;
        this.buid = customer.buid?.toLowerCase();
        this.servicecenter = customer.servicecenter?.toLowerCase();
        this.city = customer.city;
        this.state = customer.state;
        this.feeder_type = customer.feeder_type;
        this.feeder_name = customer.feeder_name;
        this.service_band = customer.service_band;
        this.dss_id = customer.dss_id;
        this.dss_name = customer.dss_name;
        this.dss_owner = customer.dss_owner;
        this.meteroem = customer.meteroem;
        this.landlord_name = customer.landlord_name;
        this.landlord_phone = customer.landlord_phone;
        this.injection_sub_station = customer.injection_sub_station;
        this.upriserid = customer.upriserid;
        this.feederid = customer.feederid;
        this.ltpoleid = customer.ltpoleid;

    }
    
    
  }
  