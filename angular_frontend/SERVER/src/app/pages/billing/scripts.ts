export class BillingScripts{
    constructor(){}
    
    public shallowSearchBilling($event) {
        try {
            var input, filter, table, tr, tds, i, txtValue;
            input = document.getElementById("billing-history-search-bar");
            filter = input.value.trim().toUpperCase();
            table = document.getElementById("billinghistory_table");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                var filterBuffer = []
               tds = tr[i].getElementsByTagName("td")
               for(let td_ of tds){
                
                    if(td_.getAttribute('hidden') == null){
                        filterBuffer.push(td_.textContent.trim())
                }
               }
               if (filterBuffer.length > 0) {
                  var strfilterBuffer = filterBuffer.join()
                  txtValue = strfilterBuffer //td.textContent + td2.textContent + td3.textContent + td4.textContent || td.innerText + td2.innerText + td3.innerText + td4.innerText
                  if (txtValue.toUpperCase().includes(filter.toUpperCase())) {
                     tr[i].style.display = "";
                  } else {
                     tr[i].style.display = "none";
                  }
               }
            }
         } catch (err) {
         }
     
     }
}