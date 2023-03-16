export interface IMeteredCaadLineItem{
    index:number;
    uuid:string;
    from_date: Date;
    to_date:Date;
    months:number;
    tarrif:number;
    present_reading:number;
    last_actual_reading:number;
    consumed:number;
    recom_unit:number;
    mab:number;
    ebm:number;
}

export interface IUNMeteredCaadLineItem{
    index:number;
    uuid:string;
    from_date: Date;
    to_date:Date;
    months:number;
    tarrif:number;
    recom_unit:number;
    mab:number;
    ebm:number;
}

export class MeteredCaadLineItem{
    index:number;
    uuid:string;
    from_date: Date;
    to_date:Date;
    months:number;
    tarrif:number;
    present_reading:number;
    last_actual_reading:number;
    consumed:number;
    recom_unit:number;
    mab:number;
    ebm:number;
    

    constructor(index,uuid){
        this.index = index
        this.uuid = uuid
    }
}

export class UnmeteredCaadLineItem{
    index:number;
    uuid:string;
    from_date: Date;
    to_date:Date;
    months:number;
    tarrif:number;
    recom_unit:number;
    mab:number;
    ebm:number;

    constructor(index,uuid){
        this.index = index
        this.uuid = uuid
    }
}