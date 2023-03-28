import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { take } from 'rxjs/operators';
import { AppState } from 'src/app/basestore/app.states';
import { LocationService } from 'src/app/services/location.service';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';
import { Locations, Location } from './models/location';
import { CreateLocations, FetchLocations } from './state/location.actions';
import { getLocations } from './state/location.selector';

AutoUnsubscribe
@Component({
  selector: 'app-locations',
  templateUrl: './locations.component.html',
  styleUrls: ['./locations.component.css']
})
export class LocationsComponent implements OnInit {
  locations$:any ;
  selectedLocation:Locations = new Locations()
  locationsData:any = []
  formActionType = 'create'
  constructor(private store: Store<AppState>,private locationService: LocationService) { 
    this.store.dispatch(new FetchLocations())
   }

  ngOnInit(): void {
    this.locations$ = this.store.select(getLocations);
    
    this.locations$.subscribe((state)=>{
      if(state.isFetched){
        this.locationsData = state.locations
        console.log(this.locationsData)
      }
      
    })

  }

  getItemById(array, id) {
    return array?.find(item => item.id == id);
  }


  getSingleLocation($event){
    this.selectedLocation = this.getItemById(this.locationsData,$event.target.id)
    this.selectedLocation = new Location(this.selectedLocation)
    console.log(this.selectedLocation)
    this.formActionType = 'edit'
    const editLocations = document.querySelector("#edit-locations")
    editLocations.classList.add('content-active')
  }

  createLocation($event){
    this.selectedLocation = new Locations()
    this.formActionType = 'create'
    const editLocations = document.querySelector("#edit-locations")
    editLocations.classList.add('content-active')
  }

  submit(){
    
    // this.selectedLocation = Object.assign({}, this.selectedLocation);
    const payload = this.selectedLocation
    console.log(payload)

    if(this.formActionType=='create'){
      this.store.dispatch(new CreateLocations(payload))
    }
    // else{this.store.dispatch()}
    this.selectedLocation = new Locations()

  }
  exitForm($event){
    const editLocations = document.querySelector("#edit-locations")
    editLocations.classList.remove('content-active')
  }

}
