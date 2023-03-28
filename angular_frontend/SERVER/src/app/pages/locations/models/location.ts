export class Locations{
    id: number;
    region;
    business_unit: string;
    service_center: string;
    BUID: string;
    service_center_address:string;   
}


export class Location{
    id;
    region;
    business_unit;
    service_center;
    BUID;
    service_center_address;
    
    constructor(payload){
        this.id = payload.id
        this.region = payload.region
        this.business_unit = payload.business_unit
        this.service_center = payload.service_center
        this.BUID = payload.BUID
        this.service_center_address = payload.service_center_address
    }
}