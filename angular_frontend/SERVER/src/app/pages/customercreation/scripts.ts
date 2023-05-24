import { environment } from 'src/environments/environment';

import { Renderer2, ComponentRef } from '@angular/core';

export function updateServicecenterValue(componentRef, newValue) {
  console.log(newValue,window['CustomercreationComponent'])
  window['CustomercreationComponent'].servicecenterdropdown.nativeElement.value = newValue.toLowerCase()
  window['CustomercreationComponent'].newCustomer.servicecenter = newValue.toLowerCase()
  // If needed, trigger change detection manually
  window['CustomercreationComponent'].cdr.detectChanges();
  console.log(window['CustomercreationComponent'].cdr.detectChanges())
}


interface CustomWindow extends Window {
  filterDropdownItems: (searchTerm: string,para:string) => void;
  setDropdownValue:(arg1,args2) => void;
  assetsTouched:any[]
}

declare let window: CustomWindow;
window.assetsTouched = []
// Helper function to set dropdown value

function clearNextDropdowns(){
  for(let id of ['dss_id','feederid','feeder_type']){
    const dropdown = document.getElementById(id);
    dropdown.setAttribute('value', '');
    dropdown.textContent = ''
  }
  
}

export async function setDropdownValue(dropdownId, value, text='N/A') {
    window.assetsTouched.push(dropdownId)
    const dropdown = document.getElementById(dropdownId);
    dropdown.setAttribute('value', value);
    dropdown.innerHTML = value.toUpperCase(); 
    if(dropdownId == 'dss_id'){
      dropdown.innerHTML = text.toUpperCase();
      // await fillFeederDropdown(value)
      await newfillFeederDropdown(value)

    }
    if(dropdownId == 'feederid'){
      dropdown.innerHTML = text;
    }

    if(dropdownId == 'dss_owner'){
      clearNextDropdowns()
      updateServicecenterValue(window['updateServiceCenterValue'],value)
    }
  }
  
window.setDropdownValue = setDropdownValue
  // Function to fill feeder dropdown based on selected DSS ID
  // {"status":true,"data":[{"assetid":"ACE10203422017119163516541","feeders":"Nbl","assettype":"33KV Feeder"}]}
export async function fillFeederDropdown(dssId) {
    const url = `${environment.api}/cms/gis/getfeeder_info?assetid=${dssId}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.status === true) {
        const feederType = data.data[0]?.assettype?.trim().replace('Feeder', '')
        const feederid = data.data[0]?.assetid;
        const feederName = data.data[0]?.feeders;
        if (data.data[0]?.assettype == undefined){
          setDropdownValue('feeder_type', 'N/A');
          setDropdownValue('feederid', 'N/A');
          return 
        }
        setDropdownValue('feeder_type', feederType);
        setDropdownValue('feederid', feederid,feederName);
      } else {
        setDropdownValue('feeder_type', 'N/A');
        setDropdownValue('feederid', 'N/A');
      }
    } catch (err) {
      console.error(err);
      setDropdownValue('feeder_type', 'N/A');
      setDropdownValue('feeder_name', 'N/A');
      // failpopupModal("No Feeder Found!!", "No Feeder was Found for this DSSID");
    }
  }

  function getItemByDssId(array, assetid) {

    return array?.find(item => item.assetid == assetid);
  }

  async function fetchISS(dss_id){
    const url = `${environment.api}/cms/gis/iss_info?dss_id=${dss_id}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.status === true) {
        return data.data
      }
      else{
        return {}
      }
    }
    catch{}
  }

  export function symLinkServiceCenters(value){
    const dss_owner_el:any = document.getElementById('dss_owner')
    if (dss_owner_el != null){
      dss_owner_el.innerHTML = value.toUpperCase()
      dss_owner_el.value = value
    }
  }

  export async function newfillFeederDropdown(dssId) {
    let dss_data =JSON.parse(window.localStorage.getItem('dss'));
    try {
       const dss_object = getItemByDssId(dss_data,dssId)
       console.log(dss_object)
        setDropdownValue('feeder_type', "");
        setDropdownValue('feederid', dss_object.FeederID,dss_object.FeederName);
        const iss = await fetchISS(dssId)
        console.log(iss)
        const injection_sub_station_el:any = document.getElementById('injection_sub_station')
        if(iss.length > 0){
          const iss_name = iss[0].INJECTION_SUBSTATION_NAME
          const feeder_type = iss[0].assettype.split(" ")[0]
          
          if(injection_sub_station_el != null){
            injection_sub_station_el.value = iss_name
          }
          setDropdownValue('feeder_type', feeder_type);
          

        }
        else{
          if(injection_sub_station_el != null){
            injection_sub_station_el.value = ''
          }
          setDropdownValue('feeder_type', '');
        }
        
     
    } catch (err) {
      console.error(err);
      setDropdownValue('feeder_type', 'N/A');
      setDropdownValue('feeder_name', 'N/A');
      // failpopupModal("No Feeder Found!!", "No Feeder was Found for this DSSID");
    }
  }

  


  
  // Function to filter dropdown items based on search input
export function filterDropdownItems(searchInput, itemList) {
  //  console.log(searchInput, itemList)
    const filter = searchInput.value.toLowerCase();
    for (const item of itemList) {
      const itemSpan = item.querySelector('span')
      if (itemSpan){
        let text = itemSpan.textContent.toLowerCase();
        if (text.indexOf(filter) > -1) {
          item.style.display = "block";
        } else {
          if (item.id !== 'exempt') {
            item.style.display = "none";
          }
        }
      }
    }
  }
window.filterDropdownItems = filterDropdownItems
  
  // Function to populate asset dropdown based on asset type and selected options
  async function populateAssetDropdown(assetType, dssOwner = '', feederType = '') {
    const id = assetType === 'dss' ? 'dss_list' : assetType === 'feeders' ? 'feederholder' : 'dss_owner_list';
    const dropdownId = '\'' + (assetType === 'dss' ? 'dss_id' : assetType === 'feeders' ? 'feederid' : 'dss_owner') + '\'';
    const nameKey = assetType === 'dss' ? 'dss_name' : assetType === 'feeders' ? 'feeders' : 'dss_owner';
    let assets = JSON.parse(window.localStorage.getItem(assetType));

    const dropdown = document.getElementById(id);
    dropdown.innerHTML = '';
    dropdown.insertAdjacentHTML('beforeend', '<li id="exempt"><input style="width:100%;height:40px;" onkeyup="window.filterDropdownItems(this, this.parentNode.parentNode.children)" placeholder="Type to search for Item" class="form-control dropdown-search" type="text"/></li>');
    console.log(assetType, dssOwner, window['CustomercreationComponent'].service_centers)
    if (assetType == 'dss_owner'){
      for (const servicecenter of window['CustomercreationComponent'].service_centers) {
        const assetOption = `<li><a href="javascript:void(0)" value="${servicecenter?.name.toLowerCase()}" onclick="setDropdownValue(${dropdownId}, this.getAttribute('value'),'${servicecenter.name}')"><span>${servicecenter.name}</span></a></li>`;
        dropdown.insertAdjacentHTML('beforeend', assetOption);
      }
    }
    
    else{
      // 
      for (const asset of assets) {
        const value = asset.assetid !== undefined ? asset.assetid : asset.dss_owner;
        const assetOption = `<li><a href="javascript:void(0)" value="${value}" onclick="setDropdownValue(${dropdownId}, this.getAttribute('value'),'${asset[nameKey]}')"><span>${asset[nameKey]}</span></a></li>`;
        dropdown.insertAdjacentHTML('beforeend', assetOption);
      }
      
    }
  }
  
  // Function to fetch GIS asset data
  
export const getGisAssetdata = async (asset_type) => {
    
    const getAttributeValue = (id) => document.getElementById(id)?.getAttribute('value');
  
    let ownerOrType = '';
    let assetKey = '';
    let cacheKey = '';
    if (asset_type === 'dss') {
      ownerOrType = getAttributeValue('dss_owner');
      assetKey = ownerOrType;
      cacheKey = 'dss_name';
    } 
    if (asset_type === 'feeders') {
      ownerOrType = getAttributeValue('feeder_type');
      assetKey = ownerOrType;
      cacheKey = ownerOrType;
    } 

    let storage;
    try {
      storage = JSON.parse(window.localStorage.getItem(asset_type));
    } catch (err) {
      storage = null;
    }
    if (storage && !storage[assetKey]) {
      storage = null;
    }
  
    if (storage) {
      await populateAssetDropdown(asset_type, ownerOrType);
    } else {
      try {
        if(asset_type != 'dss_owner'){
          const url = `${environment.api}/cms/gis/getasset_info?dss_owner=${ownerOrType}&asset_type=${asset_type}&feeder_type=${ownerOrType}`;
        const response = await fetch(url);
        const data = await response.json();
        if (data.status) {
          const newCache = data.data
          window.localStorage.setItem(asset_type, JSON.stringify(newCache));
          await populateAssetDropdown(asset_type, ownerOrType);
          if(asset_type=='dss'){
            return newCache;
          }
          else{
            return 1
          }
         
        } else {
          return data;
        }
        }
        else{
          await populateAssetDropdown(asset_type, ownerOrType);
        }
      } catch (err) {
        // Handle errors appropriately
      }
    }
  };


  
  