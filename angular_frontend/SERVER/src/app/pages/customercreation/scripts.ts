import { environment } from 'src/environments/environment';

interface CustomWindow extends Window {
  filterDropdownItems: (searchTerm: string,para:string) => void;
  setDropdownValue:(arg1,args2) => void;
}

declare let window: CustomWindow;
// Helper function to set dropdown value

function clearNextDropdowns(){
  for(let id of ['dss_id','feederid','feeder_type']){
    const dropdown = document.getElementById(id);
    dropdown.setAttribute('value', '');
    dropdown.textContent = ''
  }
  
}

export async function setDropdownValue(dropdownId, value, text='N/A') {
  
    const dropdown = document.getElementById(dropdownId);
    dropdown.setAttribute('value', value);
    dropdown.innerHTML = value;
    if(dropdownId == 'dss_id'){
      dropdown.innerHTML = text;
      await fillFeederDropdown(value)

    }
    if(dropdownId == 'feederid'){
      dropdown.innerHTML = text;
    }

    if(dropdownId == 'dss_owner'){
      clearNextDropdowns()
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
  
  // Function to filter dropdown items based on search input
export function filterDropdownItems(searchInput, itemList) {
  //  console.log(searchInput, itemList)
    const filter = searchInput.value.toLowerCase();
    for (const item of itemList) {
      console.log(item)
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
    for (const asset of assets) {
      const value = asset.assetid !== undefined ? asset.assetid : asset.dss_owner;
      const assetOption = `<li><a href="javascript:void(0)" value="${value}" onclick="setDropdownValue(${dropdownId}, this.getAttribute('value'),'${asset[nameKey]}')"><span>${asset[nameKey]}</span></a></li>`;
      dropdown.insertAdjacentHTML('beforeend', assetOption);
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
        const url = `${environment.api}/cms/gis/getasset_info?dss_owner=${ownerOrType}&asset_type=${asset_type}&feeder_type=${ownerOrType}`;
        const response = await fetch(url);
        const data = await response.json();
        if (data.status) {
          const newCache = data.data
          window.localStorage.setItem(asset_type, JSON.stringify(newCache));
          await populateAssetDropdown(asset_type, ownerOrType);
          return 1;
        } else {
          return data;
        }
      } catch (err) {
        // Handle errors appropriately
      }
    }
  };


  
  