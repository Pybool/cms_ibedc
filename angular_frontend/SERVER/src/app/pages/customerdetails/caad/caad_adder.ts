// var present_reading,last_actual_reading

// function checkFirstRowValuesExists(){
//     try{
//         let object:any = {}
//         object.present_reading = document.getElementsByClassName('present-reading')[0].value
//         object.last_actual_reading = document.getElementsByClassName('last-actual-reading')[0].value
//         if(object.present_reading.trim() == '' || object.last_actual_reading.trim()== ''){return false}
//         else{return object}
//     }
//     catch(err){return false}
    
// }

// function addCaadLineItem(self){
//     try{
//         var new_row_index:any = parseInt(document.getElementById('caad_line_items_table_last').getAttribute('value')) + 1
//         document.getElementById('caad_line_items_table_last').setAttribute('value',new_row_index)
//     }
//     catch(err){var new_row_index:any = 0}
//     try{
//         var is_metered = self.getAttribute('value')
//     }
//     catch(err){
//         var is_metered = self; //coming from update line items
//         var update = true;
//     }

//     document.getElementById('checkbox-th').style.display = 'block';
//     var checkbox = `<td class="nk-tb-col nk-tb-col-check">
//                         <div style="z-index:1;" class="custom-control custom-control-sm custom-checkbox notext ">
//                             <div class="custom-control custom-control-sm custom-checkbox notext">
//                                 <input type="checkbox" class="custom-control-input error-lineitem" id="err-flag_${new_row_index}"/>
//                                 <label class="custom-control-label" for="err-flag_${new_row_index}"></label>
//                             </div>
//                         </div>
//                     </td>`
    
//     if (is_metered == '1' || is_metered == true){
//         var object:any = checkFirstRowValuesExists()
//         var disable_recom_units = `<td class="nk-tb-cols"><input disabled="1" name='${new_row_index}' onkeyup="recomUnits(this)" class="form-control recoms" placeholder ="Enter recommended units" type="text"/></td>`
//         if (object == false){
            
//             var average_units_template =    `<td class="nk-tb-cols"><input id="" name='${new_row_index}' onkeyup="recomUnits(this)" class="present-reading form-control" placeholder ="Enter present reading" type="text"/></td>
//                                             <td class="nk-tb-cols"><input id="" name='${new_row_index}' onkeyup="recomUnits(this)" class="last-actual-reading form-control" placeholder ="Enter last actual reading" type="text"/></td>
//                                             <td class="nk-tb-cols"><input name='${new_row_index}' class="form-control consumed" readonly="1" type="text" value=""/></td>
//                                             `
//         }
//         else{
//             var average_units_template =    `<td class="nk-tb-cols"><input value="${object.present_reading}" disabled="1" id="" name='${new_row_index}' onkeyup="recomUnits(this)" class="present-reading form-control" placeholder ="Enter present reading" type="text"/></td>
//                                             <td class="nk-tb-cols"><input value="${object.last_actual_reading}" disabled="1" id="last-actual-reading" name='${new_row_index}' onkeyup="recomUnits(this)" class="last-actual-reading form-control" placeholder ="Enter last actual reading" type="text"/></td>
//                                             <td class="nk-tb-cols"><input value="${parseFloat(object.present_reading) - parseFloat(object.last_actual_reading)}" disabled="1" name='${new_row_index}' class="form-control consumed" readonly="1" type="text" value=""/></td>
//                                             `
//         }        
//     }
//     else{
//         var disable_recom_units = `<td class="nk-tb-cols"><input name='${new_row_index}' onkeyup="recomUnits(this)" class="form-control" placeholder ="Enter recommended units" type="text"/></td>`
//         var average_units_template = ''
//     }
    
//     const line_item =  `<tr id='caad-line-item_${new_row_index}' style="height:30px;background: #101924 !important;padding:5px!important;align-items:center;justify-content:center;" class="nk-tb-item is-separate" >
//                             ${checkbox}
//                             <td style="width:5%;" class="nk-tb-cols"><input name='${new_row_index}' class="form-control line_item_from_date" style="width:100%;" type="date" onchange="lineItemHandler(this);" placeholder="From date" name="from_date" class="form-control form_control" onfocus="(this.type='date')" /></td>
//                             <td style="width:5%;" class="nk-tb-cols"><input name='${new_row_index}' class="form-control line_item_to_date" style="width:100%;" type="date" onchange="lineItemHandler(this);" placeholder="To date" name="to_date" class="form-control form_control" onfocus="(this.type='date')" /></td>
//                             <td class="nk-tb-cols"><div class="caadmonths" id="caad-months"></div></td>
//                             <td class="nk-tb-cols"><select name='${new_row_index}' onchange="tarrifSelected(this)" class="form-control"><option>Select a tarrif</option><option value="24.5">24.5</option><option value="38.7">38.7</option></select></td>
//                             ${average_units_template}
//                             ${disable_recom_units}
//                             <td class="nk-tb-cols"><input name='${new_row_index}' class="form-control" readonly="1" type="text" style="" value=""/></td>
//                             <td class="nk-tb-cols"><div class="ebm" name='${new_row_index}' value="0"></div></td>
//                             <td onclick="deleteLineItem(this)"><i class="material-icons">delete</i></td>
//                         </tr>`
//     $('#caad_line_items_table').append(line_item);
//     return new_row_index
// }