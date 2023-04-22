import * as $ from "jquery";
import { environment } from 'src/environments/environment';
var tagList = []
var targets = []
var db_roles_list = []
const paths = ["accounttype","building_description","customer_category","customer_type","premise_type","supply_type","service_band"]
var position ;
// var $("#tagList") = $("#tagList");
// var $("#newTag") = $("#newTag");
// var $("#position_code") = $("#position_code");
var cache = {};

(async function (){
    try{
        var url;
        for(let path of paths){
            url = `${environment.api}/cms/settings/read_options/?type=${path}`
            await getData(url)
        }
    }
    catch(err){}
})()

export function clearTagList(){
    tagList = []
}

export function getTagList(){
    return tagList
}

export async function getData(url,awaitable=false){

    if(cache[url] !== undefined && cache[url].value.status==true && cache[url].touched == false) return cache[url].value;
    if (awaitable == true){
        await fetch(url)
        .then(response => response.json())
        .then((data) => {
            if (data.status){
                cache[url] = {time: new Date(), value: data, touched:false}
            }
            
        });
    }
    else{
        fetch(url)
        .then(response => response.json())
        .then((data) => {
            if (data.status){cache[url] = {time: new Date(), value: data, touched:false}}
            
        });
    }
    
    if (cache[url] !==undefined) return cache[url].value;
    else return {status:false,options:[]}

}
// Interval to clear cache;
setInterval(function (){
    if(Object.keys(cache).length > 0){
        let currentTime = new Date();
        Object.keys(cache).forEach(key => {
            let seconds = currentTime - cache[key].time;
            if(seconds > 120000){
                delete cache[key];
            }
        })
    }
}, 3000);

export function deleteTag(event){
    
    let self = event.target
    targets.push(self.getAttribute('value'))
    if(self.getAttribute('value') == targets[1]){
        return 
    }
     var index = $(self).parent().index();
     console.log(self.getAttribute('value'))
       
     try{

       let savebutton = document.getElementById('modal-save')
       let value =  savebutton.getAttribute('value')
       if (value.includes('_edit')){
           let Confirm = confirm("This action will permanently delete this option")
           if (Confirm){
               console.log("B4 delete ===> ", tagList)
               var url = `${environment.api}/cms/settings/options/?type=${value.split('_edit')[0]}&code=${self.getAttribute('value')}`
            
                fetch(url, { method: 'DELETE' }).then((response)=> {
                    return response.json();
                }).then((response)=> {
                 if(response.status){
                     tagList.splice(index, 1);
                     console.log("Post delete ===> ", tagList)
                     tagList_render(value);
                 }
                    return alert(`${response.message}`)
                })
                .catch((error) => {
                    alert("This operation did not complete successfully")
                });
                
              
               
           }
           else{return null}
       }
       else{
           tagList.splice(index, 1);
           tagList_render(value);   
       }
     }
     catch(err){console.log("Err===========> ", err) }
   };

export function addEventListeners(){
    document.querySelectorAll("#tagList>li>span.rmTag").forEach((node)=>{
        node.addEventListener("click",function(event){console.log(event.target);deleteTag(event)})
    })
}

function setevents(value){
    const option_item_nodes = document.querySelectorAll('.option-item');
    for (let option_item_node of option_item_nodes){
        option_item_node.addEventListener('dblclick', (e) => {
            window.localStorage.setItem('OEC',option_item_node.getAttribute('value'))
            $(option_item_node).replaceWith(`<input onkeyup ="window.handleTagEdit(this,event,'${value}')" class="edit-tag" value="${option_item_node.textContent.slice(0, -1)}"/>` );
            for (let option_item_node of option_item_nodes){option_item_node.classList.add('disabled')}
        });
    }
}

export function tagList_render (value='_new') {
  $("#tagList").empty();
  tagList.map (function (_tag) {
    value = document.getElementById('modal-save').getAttribute('value')
    if (value.includes('_edit')){
        var temp = `<li value="${_tag.code}" class="option-item">${_tag.name}<span value="${_tag.code}" class="rmTag">&times;</span></li>`;
    }
    else{var temp = `<li value="${_tag}" class="option-item-add">${_tag}<span class="rmTag">&times;</span></li>`}
        $("#tagList").append(temp);
  });
  addEventListeners()
  setevents(value)
};

function addToList(){
    let positionCodes = window.positionCodes 
     
        let positionCode = document.getElementById('position_code').value
        if(positionCodes.includes(positionCode)){

        }
        else{
            return alert("Position code was not found to be valid, position code must be one of ( RH , MD ,  RPU ,   CCU  ,  CCO  ,  HCS ,  MD , BHM ,  BHA , ADT )")
        }
    var position_code = $("#position_code").val();
        if( position_code.replace(/\s/g, '') !== '' ){
        tagList.push($("#newTag").val() + ` (${position_code})`);
        tagList_render($("#newTag").val() + ` (${position_code})`);
        document.getElementById("position_code").value = ''
        document.getElementById("newTag").value = ''
        document.getElementById("sel_position_code").value = ''
        }
}

export function renderTags (taglist,value) {
    // initial render 
    if (value == "user_positions_new" || value == "user_positions_edit"){
        document.getElementById("position_code").style.display = "block";
    }
    tagList = taglist
    tagList_render(value);
   

    // $("#position_code").on('keyup', function (e) {
    //     console.log("Taglist ===> ",tagList)
    //     if (e.keyCode == 13) {
    //       addToList()
    //     }
    // })
    // console.log($("#newTag"))
    
    
    $("#newTag").on('keyup', function (e) {
      if (e.keyCode == 13) {
        console.log("New Taglist ===> ",tagList)
        var newTag = $("#newTag").val();
        if( newTag.replace(/\s/g, '') !== '' ){
          
          if (value == "user_positions_new" || value == "user_positions_edit"){
            document.getElementById("position_code").removeAttribute('disabled')
            document.getElementById("position_code").style.opacity = 1;
            }

        else{
            tagList.push(newTag);
            $("#newTag").val('');
            tagList_render(value);
        }
          
        }
      }
    });

    addEventListeners()
    setevents(value)

  };


  export const handleTagEdit = ((self,event,value)=>{
    console.log(self,event,value)
    if (event.keyCode == 13) {
        var edittag = self.value.replaceAll("'",'')
        if( edittag.replace(/\s/g, '') !== '' ){
            var found = false;
            for(var i = 0; i < tagList.length; i++) {
                if (tagList[i].code == window.localStorage.getItem('OEC')) {
                    found = true;
                    tagList[i].name = edittag
                    break;
                }
            }
            tagList_render(value);
            setevents(value)
            const option_item_nodes = document.querySelectorAll('.option-item');
            for (let option_item_node of option_item_nodes){option_item_node.classList.remove('disabled')}
            window.localStorage.removeItem('OEC')
            }
        }
  })
  window.handleTagEdit = handleTagEdit

  export const handleCustomize = (async (value)=>{
    let customizemodal = document.querySelector("#customizeModal")
    console.log(customizemodal)
    let modaltitle = document.getElementsByClassName("modal-title")[0]
    let innertext = document.getElementById("inner-text") 
    let savebutton = document.getElementById('modal-save')
    savebutton.setAttribute('value',value)

    if (value.includes('_edit')){
        document.getElementById('newTag').style.display = "none";
        var url = `${environment.api}/cms/settings/options/?type=${value.split('_edit')[0]}`
        tagList = await getData(url,true)
        tagList = tagList.options
        if (tagList.length < 1){return alert('Could not fetch options...')}
    }
    else if (value.includes('_new')){
        document.getElementById('newTag').style.display = "block";
    }
    document.getElementById('user-settings').classList.add('user-settings')
    switch (value) {
        case 'account_type_new':
          tagList = []
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Add new account type option'
          innertext.innerHTML = 'Add new option'
          renderTags(tagList,value)
          break;

        case 'account_type_edit':
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Edit account types options'
          innertext.innerHTML = 'Remove/edit an option'
          renderTags(tagList,value)
          break;

        case 'building_description_new':
          tagList = []
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Add building description option'
          innertext.innerHTML = 'Add new option'
          renderTags(tagList,value)
          break;

        case 'building_description_edit':
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Edit building description options'
          innertext.innerHTML = 'Remove/edit an option'
          renderTags(tagList,value)
          break;

        case 'customer_category_new':
          tagList = []
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Add customer category option'
          innertext.innerHTML = 'Add new option'
          renderTags(tagList,value)
          break;
            
        case 'customer_category_edit':
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Edit customer category options'
          innertext.innerHTML = 'Remove/edit an option'
          renderTags(tagList,value)
          break;

        case 'customer_type_new':
          tagList = []
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Add customer type option'
          innertext.innerHTML = 'Add new option'
          renderTags(tagList,value)
          break;
            
        case 'customer_type_edit':
          customizemodal.classList.add('show')
          customizemodal.style.display = "block"
          modaltitle.innerHTML = 'Edit customer type options'
          innertext.innerHTML = 'Remove/edit an option'
          renderTags(tagList,value)
          break;

        case 'premise_type_new':
            tagList = []
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Add premise type option'
            innertext.innerHTML = 'Add new option'
            renderTags(tagList,value)
            break;
              
        case 'premise_type_edit':
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Edit premise type options'
            innertext.innerHTML = 'Remove/edit an option'
            renderTags(tagList,value)
            break;
        
        case 'supply_type_new':
            tagList = []
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Add supply type option'
            innertext.innerHTML = 'Add new option'
            renderTags(tagList,value)
            break;
                
        case 'supply_type_edit':
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Edit supply type options'
            innertext.innerHTML = 'Remove/edit an option'
            renderTags(tagList,value)
            break;
        
        case 'service_band_new':
            tagList = []
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Add service band option'
            innertext.innerHTML = 'Add new option'
            renderTags(tagList,value)
            break;
                
        case 'service_band_edit':
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Edit service band options'
            innertext.innerHTML = 'Remove/edit an option'
            renderTags(tagList,value)
            break;

        case 'user_positions_new':
            tagList = []
            document.getElementById('user-settings').classList.remove('user-settings')
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Add New Positions'
            innertext.innerHTML = 'Add new option'
            document.getElementById('position-cart').style.display = 'block'
            renderTags(tagList,value)
            break;
                
        case 'user_positions_edit':
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Edit Positions'
            innertext.innerHTML = 'Remove/edit an option'
            document.getElementById('position-cart').style.display = 'none'
            renderTags(tagList,value)
            break;

        case 'caad_vat_new':
            tagList = []
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Add New Vat option'
            innertext.innerHTML = 'Add new option'
            renderTags(tagList,value)
            break;
                
        case 'caad_vat_edit':
            customizemodal.classList.add('show')
            customizemodal.style.display = "block"
            modaltitle.innerHTML = 'Edit Vat options'
            innertext.innerHTML = 'Remove/edit an option'
            renderTags(tagList,value)
            break;
        
      }
  })

  window.handleCustomize  = handleCustomize
  window.addToList = addToList
  window.toProperCase =  String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
  };

  export const saveOptions = (async (self)=>{
    let data = []
    let value = self.getAttribute('value')
    let option_item_nodes = document.getElementsByClassName('option-item-add')
    for (let option_item of option_item_nodes){
        data.push(option_item.getAttribute('value'))
    }
    const precedence = document.getElementById('precedence').value;
    const process_code = document.getElementById('sel_position_code').value;
    if (paths.includes(value.split('_new')[0]) == false){
        if (precedence !== '-1' && process_code !== '0'){
            data.push({precedence:precedence,process_code:process_code})
        }
    }
    console.log("======> ",data, option_item_nodes)
    
    if (value.includes('_new')){
        if (data.length > 0){
            var url = `${environment.api}/cms/settings/create_options/?type=${value.split('_new')[0]}&data=${JSON.stringify(data)}`
            var geturl = `${environment.api}/cms/settings/read_options/?type=${value.split('_new')[0]}`
            await fetch(url).then((response)=> {
                return response.json();
                }).then((data)=> {
                    if (data.status){
                        try{
                            tagList = []
                        }
                        catch(err){}

                        if(cache[geturl] !== undefined && cache[geturl].value.status==true && cache[geturl].touched == false){
                            cache[geturl].touched = true
                        }
                    }
                    
                    alert(`${data.message}`)
            })
        
        }
        else{alert("No option is populated...")}
        
    }
    else if (value.includes('_edit')){
        var url = `${environment.api}/cms/settings/update_options/?type=${value.split('_edit')[0]}&data=${JSON.stringify(tagList)}`
        var geturl = `${environment.api}/cms/settings/read_options/?type=${value.split('_edit')[0]}`
        await fetch(url).then((response)=> {
            return response.json();
            }).then((data)=> {
                if (data.status){
                    try{
                        tagList = []
                        console.log("",cache,geturl,cache[""+geturl])
                    }
                    catch(err){}
                    if(cache[""+geturl] !== undefined && cache[""+geturl].value.status==true && cache[""+geturl].touched == false){
                        cache[""+geturl].touched = true
                    }
                }
                alert(`${data.message}`)
        })
    }
    
  })

export function modalclose(){
    let customizemodal = document.querySelector("#customizeModal")
    customizemodal.classList.remove('show')
    customizemodal.style.display = "none"
    document.getElementById('position-cart').style.display = 'none'
}

export async function deleteRole(position_code,process_code){
    var url = `${environment.api}/cms/settings/delete_role_hierarchy/?position_code=${position_code}&process_code=${process_code}`
    await fetch(url).then((response)=> {
        return response.json();
        }).then((data)=> {
            if (data.status){
                alert(`${data.message}`)
            }
    })
}

export async function removeTag(self,process_code,id){
    // alert(id)
    try{
        var db_roles = JSON.parse(document.getElementById(`${id}`).getAttribute('value').replaceAll("'",'"'))
    }
    catch(err){var db_roles = []}
    if (db_roles_list.length == 0 && db_roles.length != 0){
        for (let db_role of db_roles){
            db_roles_list.push(db_role.position_code)
        }
    }
    if (db_roles_list.includes(self.getAttribute('value'))){
        await deleteRole(self.getAttribute('value'),process_code)
        
        const index = db_roles_list.indexOf(self.getAttribute('value'));
        if (index > -1) { // only splice db_roles_list when item is found
            db_roles_list.splice(index, 1); // 2nd parameter means remove one item only
        }
        return self.parentNode.remove()
    }
    self.parentNode.remove()
}

export async function saveRolePrecedence(data,process_code){
    var url = `${environment.api}/cms/settings/update_role_hierarchy/?data=${JSON.stringify(data)}&process_code=${process_code}`
    await fetch(url, { method: 'PUT' }).then((response)=> {
        return response.json();
        }).then((data)=> {
            if (data.status){
                alert(`${data.message}`)
            }
    })
}

export async function saveRoles(process_code,template_precendence){
    let nodes;
    let data = []
    nodes = document.getElementsByClassName(`${template_precendence}`)
    for(let node of nodes){
        if (node.value == ''){return alert(`${node.name} precedence code is required...`)}
        data.push({process_code:process_code,position_code:node.name,precedence:node.value})
    }
    await saveRolePrecedence(data,process_code)
}
window.saveRoles = saveRoles

export function add_selection_to_tag(self,id,li_class,process_code,template_precendence,dbroles){ 
    let nodes;
    var $users_tagList = $(`#${id}`);
    var temp = `<li value="${self.value}" class="option-item ${li_class}">${self.value}<span value="${self.value}" onclick="removeTag(this,'${process_code}','${dbroles}')" class="rmTag">&times;</span>
                    <input style="text-align:center;border-radius:13px;background:white!important;padding:5px;" name="${self.value}" class="${template_precendence}" placeholder="Enter precedence code" required="1" type="text"/>
                </li>
                `
    nodes = document.getElementsByClassName(`${li_class}`)
    for(let node of nodes){
        if (self.value == Array.from(node.attributes)[1].value){
            return null
        }
    }
    $users_tagList.append(temp)
}

window.add_selection_to_tag  = add_selection_to_tag
