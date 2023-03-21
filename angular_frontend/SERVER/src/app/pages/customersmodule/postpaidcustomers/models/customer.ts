export class EMSCustomer{
    accountno?: string;
    oldaccountnumber?: string | null;
    meterno?: string | null;
    surname?: string | null;
    firstname?: string | null;
    othernames?: string | null;
    address1?: string | null;
    address2?: string | null;
    city?: string | null;
    state?: string | null;
    email?: string | null;
    serviceaddress1?: string | null;
    serviceaddress2?: string | null;
    serviceaddresscity?: string | null;
    serviceaddressstate?: string | null;
    tariffid: number | null;
    arrearsbalance: number | null;
    mobile?: string | null;
    vat?: boolean | null;
    applicationdate?: Date | null;
    placeofwork?: string | null;
    addressoforganisation?: string | null;
    giscoordinate?: string | null;
    guarantorname?: string | null;
    guarantoraddress?: string | null;
    setupdate?: Date | null;
    connectdate?: Date | null;
    distributionstation?: string | null;
    injectionstation?: string | null;
    upriserno: number | null;
    utid?: string | null;
    buid?: string | null;
    transid?: string | null;
    statuscode?: string | null;
    storedaverage: number | null;
    connectiontype?: string | null;
    distributionid?: string | null;
    backbalance?: number | null;
    customerid?: string | null;
    accounttype?: string | null;
    newtariffcode?: string | null;
    dss_id?: string | null;
    servicecenter?: string | null;
    updated_at?: string;
    kyc?: string | null;
    title?: string | null;
    gender?: string | null;
    building_description?: string | null;
    lga?: string | null;
    premise_type?: string | null;
    region?: string | null;
    customer_type?: string | null;
    business_type?: string | null;
    feeder_name?: string | null;
    service_band?: string | null;
    contactname?: string | null;
    contactphone?: string | null;
    contactemail?: string | null;
    landlord_name?: string | null;
    landlord_phone?: string | null;
    tenant?: string | null;
    landlord?: string | null | undefined;
    injection_sub_station?: string | null | undefined;
    cin?: string | null | undefined;
    meteroem?: string | null | undefined;
    upriserid?: string | null | undefined;
    feederid?: string | null | undefined;
    ltpoleid?: string | null | undefined;
    latitude?: string | null | undefined;
    longitude?: string | null | undefined;
  
}


export class CustomerFilter {
  accounttype?:boolean;
  kyc?:string;
  statuscode?:string;
  dss_id?:string;
  feeder_name?:string;
  state?: string[];
  buid?: string;
  servicecenter?: string;
  start_date?: string;
  end_date?: string;


}
