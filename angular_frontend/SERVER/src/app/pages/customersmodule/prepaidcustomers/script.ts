export class Customers{
    constructor(){}

    public ensureComplete(){
        const kyc = document.getElementById('kyc_filter').getAttribute('value')
        const accounttype = document.getElementById('account_type_filter').getAttribute('value')
        const statuscode = document.getElementById('status_code_filter').getAttribute('value')
        if (kyc && accounttype && statuscode != null){
            let data = {kyc:kyc,accounttype:accounttype,statuscode:statuscode}
            return [true, data]
        }
        return [false,{}]
        
    }
    
    public customerfilterSearch = async ()=>{
        let response = this.ensureComplete()
        let status = response[0]
        let data = response[1]
        if (!status) return alert('Filter fields must be completed')
        document.getElementById('loader').style.display = 'block'
    }

    public searchCustomer($event) {
        try {
           var view_mode = 'list'//window.localStorage.getItem('cust_view_mode')
           
           if (view_mode == "list") {
             var input, filter, table, tr, tds, i, txtValue;
             
             input = $event.target
             filter = input.value.toUpperCase();
             table = document.getElementById("customer_table");
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
          }
     
           if (view_mode == "grid") {
              let input, filter, grid, div, td, i, txtValue, accountno, custname, abbr_name, divt;
              input = document.getElementById("search_bar_input");
              filter = input.value.toUpperCase();
              grid = document.getElementById("customers_grid");
              for (i = 0; i < grid.childElementCount; i++) {
                 div = grid.children[i]
                 divt = div.getElementsByTagName("div")[7];
                 accountno = div.getElementsByClassName("kanban_accno")[0]
                 custname = div.getElementsByClassName("custname")[0]
                 abbr_name = div.getElementsByClassName("abbr_name")[0]
                 if (accountno) {
                    txtValue = accountno.textContent + custname.textContent + abbr_name.textContent || accountno.innerText + custname.innerText + abbr_name.innerText
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                       div.style.display = "";
                    } else {
                       div.style.display = "none";
                    }
                 }
     
              }
           }
        } catch (err) {
          console.log(err)
        }
     
     }
     
}