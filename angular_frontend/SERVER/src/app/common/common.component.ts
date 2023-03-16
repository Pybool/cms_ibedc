import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
declare function myfunction(): any;

@Component({
  selector: 'app-common',
  templateUrl: './common.component.html',
  styleUrls: ['./common.component.css']
})
export class CommonComponent implements OnInit {

  title = 'cms-ibedc-app';
  usersMail= ''
  usersName = ''
  constructor(private router: Router){
    
  }

  ngOnInit(){
    console.log('configured routes: ', this.router.config);
  }

  darkMode(){

  }

  abbreviateName(usersName){

  }

  searchBarFilter(val){

  }

ngAfterViewInit() {
  
  try{
    myfunction()
  }
  catch(err:any){
    
  }
  
  
}
}
