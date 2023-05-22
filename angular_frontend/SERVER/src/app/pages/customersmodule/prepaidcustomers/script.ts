import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
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
           var view_mode = window.localStorage.getItem('cust_view_mode')
           
           if (view_mode == "list") {
             var input, filter, table, tr, tds, i, txtValue;
             
             input = $event.target
             filter = input.value.trim().toUpperCase();
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
              input = $event.target
              filter = input.value.toUpperCase();
              grid = document.getElementById("kanban-wraps");
              for (i = 0; i < grid.childElementCount; i++) {
                 div = grid.children[i]
                 let spans = div.getElementsByTagName("span");
                 if (accountno) {
                    txtValue = spans[1].textContent + spans[2].textContent + spans[4].textContent + spans[5].textContent + spans[6].textContent
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


// Themes begin
// function renderDoughnut(){
//    am4core.useTheme(am4themes_animated);
//    // Themes end
 
//    // Create chart instance
//    var chart = am4core.create("chartdiv", am4charts.PieChart);  
 
//    function doughnutchartData(default_data){
//      try{
//        nodes = document.getElementsByClassName('chartdiv')
     
//        var attr = nodes[0].getAttributeNames().reduce((acc, name) => {
//            return {...acc, [name]: nodes[0].getAttribute(name)};
//          }, {})
       
//        var data_ = attr.value
//        data_ = data_.replaceAll("'",'"')
//        data_ = JSON.parse(data_)
//        console.log("1",data_)
//        // data_= data_.map(entry =>
//        //   Object.entries(entry).reduce(
//        //         (obj, [key, value]) => (!isNaN(parseFloat(value)) && !value.includes('-') ? obj[key] = parseFloat(value)  : obj[key] = value, obj),
//        //         {}
//        //     )
//        // );
//        console.log("2",data_)
//        default_data[0]['m_count'] = data_.meters_installed
//        default_data[1]['m_count'] = data_.meter_pending_installs
//        default_data[2]['m_count'] = data_.new_requests_for_install
//        if (data_.meters_installed==0 && data_.meter_pending_installs==0 && data_.new_requests_for_install==0){
       
//            var nodes_ = document.getElementsByClassName('chartdiv')
//            nodes_[0].innerHTML = "No data available for this period"
         
//        }
//        if (data_.meters_installed==null && data_.meter_pending_installs==null && data_.new_requests_for_install==null){
       
//          var nodes_ = document.getElementsByClassName('chartdiv')
//          nodes_[0].innerHTML = "No data available for this period"
       
//      }
//        return default_data
       
//      }
//      catch(err){}
     
     
//    }
 
//    // Add data
//    let default_data = [ {
//                          "description": "Meters installed",
//                          "m_count": 1,
//                          "color": am4core.color("#6771dc")
//                        }, {
//                          "description": "Pending Installation",
//                          "m_count": 1,
//                          "color": am4core.color("#67b7dc")
//                        }, {
//                          "description": "New requests",
//                          "m_count": 1,
//                          "color": am4core.color("#dc67ce")
//                        }]
//    chart.data = doughnutchartData(default_data)
 
//    // Set inner radius
//    chart.innerRadius = am4core.percent(60);
 
//    //Add label
//    var label = chart.seriesContainer.createChild(am4core.Label);
//    label.text = "";
//    label.horizontalCenter = "middle";
//    label.verticalCenter = "middle";
//          //  label.fontSize = 50;
 
//    // Add and configure Series
//    var pieSeries = chart.series.push(new am4charts.PieSeries());
//    pieSeries.dataFields.value = "m_count";
//    pieSeries.dataFields.category = "description";
//    pieSeries.slices.template.stroke = am4core.color("#fff");
//    pieSeries.slices.template.strokeWidth = 2;
//    pieSeries.slices.template.propertyFields.fill = "color";
//    pieSeries.slices.template.strokeOpacity = 1;
//    pieSeries.ticks.template.disabled = true;
//    pieSeries.labels.template.disabled = true;
 
//    // This creates initial animation
//    pieSeries.hiddenState.properties.opacity = 1;
//    pieSeries.hiddenState.properties.endAngle = -90;
//    pieSeries.hiddenState.properties.startAngle = -90;
//    // $('g:has(> g[aria-labelledby="id-66-title"])').hide();
 
//    (function($) { 
//      $(function() { 
 
//        //  open and close nav 
//        $('#navbar-toggle').click(function() {
//          $('nav ul').slideToggle();
//        });
 
//        // Hamburger toggle
//        $('#navbar-toggle').on('click', function() {
//          this.classList.toggle('active');
//        });
 
//        // If a link has a dropdown, add sub menu toggle.
//        $('nav ul li a:not(:only-child)').click(function(e) {
//          $(this).siblings('.navbar-dropdown').slideToggle("slow");
 
//          // Close dropdown when select another dropdown
//          $('.navbar-dropdown').not($(this).siblings()).hide("slow");
//          e.stopPropagation();
//        });
 
 
//        // Click outside the dropdown will remove the dropdown class
//        $('html').click(function() {
//          $('.navbar-dropdown').hide();
//        });
//      }); 
//    })(jQuery); 
//  }
 