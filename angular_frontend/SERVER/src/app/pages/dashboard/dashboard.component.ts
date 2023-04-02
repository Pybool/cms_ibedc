import { Component, OnDestroy, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { UserState } from 'src/app/authentication/state/auth.selector';
import { AppState } from 'src/app/basestore/app.states';
import { DashboardService } from 'src/app/services/dashboard.service';
import { SharedService } from 'src/app/services/shared.service';
import { AutoUnsubscribe } from 'src/auto-unsubscribe.decorator';
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5percent from "@amcharts/amcharts5/percent";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";


@AutoUnsubscribe
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnDestroy {
  Math
  period = '1'
  cuid = 0
  start_date;
  end_date;
  userState;
  obs1;
  obs2;
  obs3;
  opsmanager;
  accounts_data;
  feeders_data;
  feedersSum;
  todayCollections;
  todayCollectionsSum;
  collectionsStatistics;
  recent_payments;
  metering_stats_data;
  today_collections_breakdown:string ="N/A";


  constructor(private store: Store<AppState>,private sharedService:SharedService, private dashboardService: DashboardService) { 
    let payload
    const today = new Date();
    this.start_date = today.toISOString().slice(0, 10);
    this.end_date = today.toISOString().slice(0, 10);
    this.sharedService.setActiveSearchInput('payments')
    this.userState = this.store.select(UserState);
    this.userState.subscribe((user)=>{
      console.log('user id ', user.id)
      if(user.id){
        this.cuid = user.id
        payload = {period:this.period,cuid:this.cuid,end_date:this.end_date,start_date:this.start_date}
        this.obs1 = this.dashboardService.fetchAccountsFeedersAndRecentPayments(payload).subscribe((response)=>{
          if(response.status){
            this.accounts_data = response.data?.accounts_data
  
            this.feeders_data = response?.feeders 
            console.log(Object.values(response?.feeders))
            this.feedersSum = Object.values(response?.feeders[0])?.reduce((accumulator:number, currentValue:number) => accumulator + currentValue, 0);
            this.recent_payments = response?.data.recent_payments
            this.removeSkeleton(["prepaid_count","postpaid_count","feeders_count","recent_payments_card"])
          }
        })
        this.obs2 = this.dashboardService.fetchCollectionStatisticsAndOpsmanager(payload).subscribe((response)=>{
          if(response.status){
            this.opsmanager = response.data?.ops_manager
            this.collectionsStatistics = response.data?.collection_statistics
            console.log(this.opsmanager)
            this.plotGraph()
            if(this.collectionsStatistics.length == 0){
              document.querySelector('#chartdiv').textContent = 'No collections statistics data was found '
            }
            this.removeSkeleton(["today_collections_count","chartdiv","ops_data"])
            // console.log("Collections stats available ===> ", this.collectionsStatistics)
          }
          else{}
        })
        this.obs3 = this.dashboardService.fetchTodaysCollectionsAndMeteringStatistics(payload).subscribe((response)=>{
          let dict = {}
          let today_collections_breakdownList = []
          if(response.status){
            this.todayCollections = response.today_cols_data
            this.metering_stats_data = response.metering_stats_data
            this.renderDoughnut()
            this.todayCollectionsSum = this.todayCollections?.reduce((acc, obj) => acc + (obj.today_collections || 0), 0);
            this.todayCollections.forEach((data)=>{
              today_collections_breakdownList.push(`${this.titleCase(data?.type)}: ₦ ${data.today_collections?.toLocaleString('en-US')}`) 
            })
            console.log(today_collections_breakdownList.join(" "))
            this.today_collections_breakdown =today_collections_breakdownList.join(" ")
            this.removeSkeleton(["today_collections_count"])
            document.querySelector("#today-collections-card").setAttribute("data-bs-original-title",this.today_collections_breakdown)
          }
        })
      }
      
    })
  }

  titleCase (str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
  }

  ngAfterViewInit(){
    
  }

  round(val){
    try{
      console.log(val)
    return Math.round(parseInt(val))
    }
    catch(err){console.log(err)}
    
  }

  removeSkeleton(ids){
    ids.forEach((id)=>{
      let el = document.getElementById(id)
      el.classList.remove('post-skeleton-show')
      const parentCard = el.closest('.card');
      parentCard.classList.remove('skeleton-box')
    })
    
  }

  ngOnInit(): void {
    (function(){
      const dropdowns = document.querySelectorAll('.dropdown');
      const dropups = document.querySelectorAll('.dropup');
      dropdowns.forEach(dropdown => {
          dropdown.addEventListener('mouseover', function hoverOn(event) {
              try{dropdown.children[1].classList.add('show');}
              catch{}
          });
          dropdown.addEventListener('mouseout', async function hoverOut(event) {
              try{dropdown.children[1].classList.remove('show');}
              catch{}
          });
      });
      
      dropups.forEach(dropup => {
          dropup.addEventListener('mouseover', function hoverOn(event) {
              dropup.children[1].classList.add('show');
          });
          dropup.addEventListener('mouseout', async function hoverOut(event) {
              
              dropup.children[1].classList.remove('show');
          });
      });
    })()
  }

  loadCustomerInformation($event,accountno,meterno,accounttype){
    let base = `customer/information/basic-information`
    const queryParams = {accountno : accountno, accounttype: accounttype?.toLowerCase(),meterno:meterno };
    this.sharedService.navigateWithParams(base,queryParams)
  }

  handler(){

  }

  private plotGraph() {
    // this.uid = this.tokenstorageservice.getUser()
          // Create chart instance
          
      const colors = [ "#007bff", "#6610f2","#6f42c1","#e83e8c","dc3545",
                        "#fd7e14","#ffc107","#28a745","#20c997","#17a2b8","#6c757d","#343a40",
                        "#007bff","#6c757d","#28a745","#17a2b8","#ffc107","#dc3545","#f8f9fa", "#343a40"
                      ]
     
      // Create root and chart
      let root = am5.Root.new("chartdiv");
      // let chart = root.container.children.push( 
      //   am5xy.XYChart.new(root, {
      //     panY: false,
      //     layout: root.verticalLayout
      //   }) 
      // );

      let chart = root.container.children.push( 
        am5xy.XYChart.new(root, {
          panX: true,
          panY: true,
          wheelX: "panX",
          wheelY: "zoomX",
          pinchZoomX:true
        }) 
      );

    
      // Add cursor
      // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
      var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
      cursor.lineY.set("visible", false);

      
      
      // Create axes
      // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
      var xRenderer = am5xy.AxisRendererX.new(root, { minGridDistance: 30 });
      xRenderer.labels.template.setAll({
        rotation: -90,
        centerY: am5.p50,
        centerX: am5.p100,
        paddingRight: 15
      });

    
      
      var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
        maxDeviation: 0.3,
        categoryField: "period",
        renderer: xRenderer,
        tooltip: am5.Tooltip.new(root, {})
      }));

     
      var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        maxDeviation: 0.3,
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      
      // Create series
      // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
      var series = chart.series.push(am5xy.ColumnSeries.new(root, {
        name: "Series 1",
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "value",
        sequencedInterpolation: true,
        categoryXField: "period",
        tooltip: am5.Tooltip.new(root, {
          labelText:"{valueY}"
        })
      }));

    
      
      series.columns.template.setAll({ cornerRadiusTL: 5, cornerRadiusTR: 5 });
      series.columns.template.adapters.add("fill", function(fill, target) {
        return chart.get("colors").getIndex(series.columns.indexOf(target));
      });

     
      series.columns.template.adapters.add("stroke", function(stroke, target) {
        return chart.get("colors").getIndex(series.columns.indexOf(target));
      });

      
      var data = this.collectionsStatistics.sort((a, b) => (a.period > b.period) ? 1 : -1);;
     
      console.log("Barchart data ",data)
      xAxis.data.setAll(data);
      series.data.setAll(data);
      

      
      // Make stuff animate on load
      // https://www.amcharts.com/docs/v5/concepts/animations/
      series.appear(1000);
      chart.appear(1000, 100);


      //Events handling to split each axes
      xAxis.get("renderer").labels.template.setup = function(target) {
        target.set("background", am5.Rectangle.new(root, {
          fill: am5.color(0xff0000),
          fillOpacity: 0
        }))
      }


      
  }

  renderDoughnut(){
    // Create root and chart
  let root:any = am5.Root.new("doughnut");
  root.setThemes([
    am5themes_Animated.new(root)
  ]);
  
  let chart = root.container.children.push( 
    am5percent.PieChart.new(root, {
      radius: am5.percent(60),
      // x: am5.percent(50),
    innerRadius: am5.percent(70),
    }) 
  );
  chart.appear(1000);

  // Define data
  
  let y = []

Object.keys(this.metering_stats_data[0]).forEach((x)=>{
  let c = {}
  c['type'] = this.titleCase(x.replaceAll('_',' '))
  c['value'] = this.metering_stats_data[0][x]
  y.push(c)
})
let data = y
console.log("------>",data)
this.removeSkeleton(['metering'])


  // Create series
  let series = chart.series.push(
    am5percent.PieSeries.new(root, {
      name: "Series",
      valueField: "value",
      categoryField: "type",
      legendLabelText: "[{fill}]{category}[/]",
    legendValueText: "[bold {fill}]{value}[/]"
    })
  );
  series.ticks.template.set("visible", true);
  series.slices.template.set('tooltipText', '{category}: {value}');
series.labels.template.set('text', '{category}: {value}');
series.appear(1000);
series.data.setAll(data);


// Add legend

let legend = chart.children.unshift(am5.Legend.new(root, {
  centerX: am5.percent(50),
  x: am5.percent(50),
  innerRadius: am5.percent(50),
  layout: root.verticalLayout
}))


legend.data.setAll(series.dataItems);
  }

  ngOnDestroy(): void {
    
  }

  
  
}


