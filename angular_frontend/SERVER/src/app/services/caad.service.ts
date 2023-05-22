import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AppState } from '../basestore/app.states';

@Injectable({
  providedIn: 'root'
})
export class CaadService {
  listOrCreate$:any = new BehaviorSubject<Boolean>(false);
  CaadSucess$:any = new BehaviorSubject<Boolean>(false);

  constructor(private store: Store<AppState>,
              private http: HttpClient,
              private router: Router
              ){ }

  
  public setListOrCreate(status){
    this.listOrCreate$.next(status)
  }
             
  public getListOrCreate(){
    return this.listOrCreate$.asObservable()
  }

  public setCaadSucess(status){
    this.CaadSucess$.next(status)
  }

  public getCaadSucess(){
    return this.CaadSucess$.asObservable()
  }

  
  fetchCaadList(){
    return this.http.get<any>(`${environment.api}/cms/caadlist`)
  }

  fetchCaadLineItems(id){
    return this.http.get<any>(`${environment.api}/cms/caadlist?id=${id}`)
  }

  getErrorRows(){
    var errorLineItems = []
    var inputs = document.querySelectorAll('.error-lineitem');   
        for (var i = 0; i < inputs.length; i++) { 
            // if (inputs[i].checked){errorLineItems.push(parseInt(inputs[i].closest('tr').getAttribute('value')))}  
        }  
        return errorLineItems 
  }
  

  caadApproval(header,action,revert_comments=null){
      // Action codes = {'0':'Revert','1':'Approve','2':'Validate'}
      // if (action == 0){
      //     let revertComment = document.getElementById('caad-revert-comment').value.trim() 
      //     if (revertComment == ''){
      //         return alert('You must provide a reason for reverting this caad record...')
      //     }
      //     else{
      //         let errorLineItems = this.getErrorRows()
      //         var url = `${''}/cms/caad/approval/?data=${JSON.stringify({header:header,revert_comments:revertComment,action:action,error_lineitems:errorLineItems})}`
      //         fetch(url).then((response)=> {
      //             return response.json();
      //         }).then((data)=> {
      //             var modal = document.getElementById('modalAlert')
      //             var title = document.getElementById('success-title')
      //             var msg = document.getElementById('success-msg')
      //             var subMsg = document.getElementById('success-sub-msg')
      //             title.innerHTML = `Success!!`
      //             msg.innerHTML = `This caad record has been reverted `
      //             subMsg.innerHTML = `.`
      //             modal.classList.add('show')
      //             modal.style.display = 'block'
      //             modal.setAttribute('aria-hidden',false)
      //         })
      //     }
      // }
  
      if(action == 0 || action == 1){
          return this.http.put<any>(`${environment.api}/cms/caadlist?action=${action}`,{header:header,action:action,revert_comments:revert_comments})
      }
      return of({status:false,message:"Invalid action specified"})
  }
  
}
