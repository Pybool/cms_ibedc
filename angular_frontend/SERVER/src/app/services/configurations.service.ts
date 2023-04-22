import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationsService {
  metaData$:any = new BehaviorSubject<any>({});

  constructor(private http: HttpClient) { 
    this.getConfigData().subscribe((data)=>{
      this.metaData$.next(data) 
      console.log(data)
    })
  }

  public getUserSettingsMetaData(){

    return this.metaData$.asObservable()
  }

  createPositionCode(payload){
    return this.http.post<any>(`${environment.api}/cms/settings/position_codes`,payload)
  }

  getPositionCodes(){
    return this.http.get<any>(`${environment.api}/cms/settings/position_codes`)
  }

  deletePositionCode(id){
    return this.http.delete<any>(`${environment.api}/cms/settings/position_codes?id=${id}`)
  }
  

  createConfigOption(payload:any){
    return this.http.post<any>(`${environment.api}/cms/settings/create_options`,payload)
  }

  getConfigData(){
    return this.http.get<any>(`${environment.api}/cms/settings/getdata`)
  }

  updateConfigOption(payload:any){
    return this.http.put<any>(`${environment.api}/cms/settings/update_options`,payload)
  }

  

}
