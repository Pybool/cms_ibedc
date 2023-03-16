async function msdelay(ms) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }
const renderCustomersTable = ((data)=>{
    var customerWorker = new Worker("/cms_ibedc/static/src/js/customer_table_worker.js")
    console.log(document.getElementById('create-perm').value)
    customerWorker.postMessage({"args": [data,window.localStorage.getItem('switchMode'),document.getElementById('create-perm').value]})
    customerWorker.onmessage = function(e){
        
        customerWorker.terminate()
        customerWorker = undefined
        var template = e.data.template[0]
        

        let p = new Promise((resolve,reject)=>{
            $('#custtable-spinner').remove()
            document.getElementById('customers_table').innerHTML = ''
            $('#customers_table').append(template);  
            console.log("Worker returned ")          
            resolve()
        })
        p.then(()=>{
            try{
                console.log("starting conversion ...")
                new DataTable('#customers_table', {
                    "pageLength": 50,"bPaginate": true,
                    "responsive": true,
                    processing: true,
                    "searching":false,
                    "bdeferRender": true,
                    "destroy":true,
                    dom: 'Bfrtip',
                    buttons: [
                        'copy', 'csv', 'excel', 'pdf', 'print'
                    ]
                });
                
                console.log("Converted to datatable")
                if(window.localStorage.getItem('switchMode')=='dark'){
                    // waitForElm('#customers_table_wrapper').then((elm) => {
                    //     document.getElementById('customers_table').classList.add('table-dark')
                    // })
                    try{
                        waitForElm('#customers_table_wrapper').then((elm) => {
                            var node = document.getElementById('customers_table_wrapper')
                            node.style.backgroundColor = "#101924"
                            node.color= "#b6c6e3"
                        })
                        }
                        catch{}
                }
            }
            catch(err){alert(err) } 
        })
        
        return template
    }

}) 