// import { Component } from '@angular/core';


// export class PaginationComponent {

// }

// import { Component } from '@angular/core';
// import { PaginationService } from 'src/app/services/pagination.service';
// // import { PaginationService } from './pagination.service';

// @Component({
//   selector: 'app-pagination',
//   template: `
//     <ul>
//       <li *ngFor="let link of links">
//         <a *ngIf="link.page" [routerLink]="link.link" [class.active]="link.page === currentPage">{{ link.page }}</a>
//         <span *ngIf="!link.page">{{ link.link }}</span>
//       </li>
//     </ul>
//   `,
// })


import { Component, ElementRef, Renderer2 } from '@angular/core';
import { ConvertTableService } from 'src/app/services/convert-table.service';
import { CustomerService } from 'src/app/services/customer.service';
import { PaginationService } from 'src/app/services/pagination.service';
import { SharedService } from 'src/app/services/shared.service';
import { SpinnerService } from 'src/app/services/spinner.service';
// import { PaginationService } from './pagination.service';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent {
  links: Array<any>;
  currentPage: number;
  totalPages: number;
  displayedPages 
  showLoadMoreButton:boolean = true
  activateLessButton:boolean = false
  firstrun = true
  cap = 2000
  isCallable = true
  blocks = this.generateMultiplesOfThree(0,400)
  scrollContainer: HTMLElement; // a reference to the scroll container element
  activePage

  constructor(private paginationService: PaginationService,
    private elRef: ElementRef, private renderer: Renderer2,
    private customerService: CustomerService,private convertTableService: ConvertTableService,
    private spinnerService: SpinnerService,private sharedService: SharedService) {
  }


  generateMultiplesOfThree(start = 0, stop = 0, chunk = 400) {
    if (stop > start) {
      chunk = stop - start;
    }
    const len = Math.round(chunk / 3);
    const numbers = new Array(len);
    for (let i = 0; i < len; i++) {
      numbers[i] = (i * 3) + start;
    }
    return numbers;
  }

  ngOnInit() {
    const firstLink = 'https://example.com/api?page=1';
    const lastLink = 'https://example.com/api?page=240';
    console.log("=======================",'response')

    this.paginationService.generateLinks$().subscribe((response)=>{
      console.log("=======================",response)
      this.links = response.links
      try{
        this.displayedPages = this.links.slice(0,5)
      console.log(this.links)
      this.currentPage = this.paginationService.getCurrentPage();
      this.totalPages = this.paginationService.getTotalPages();
      }
      catch{}
    });
    // this.originalLinks = this.links
    
  }

  ngAfterViewInit() {
    this.scrollContainer = this.elRef.nativeElement.querySelector('.scroll-container');
  }

  onScroll(event) {
    const element = event.target;
    if ((Math.round(element.scrollHeight - element.scrollTop) - element.clientHeight) < 2) { // This works for exact precision Math.round(element.scrollHeight - element.scrollTop) === element.clientHeight
      this.loadMoreItems();
    }
  }

  getSiblings = node => [...node.parentNode.children].filter(c => c !== node)


  nextPage($event,link,cmp){
    console.log(link,cmp)
    // const parentElement = document.getElementById('table-wrapper');
    // console.log("---------> ", parentElement)
    // this.spinnerService.showSpinner(parentElement);
    // this.sharedService.setSpinnerText('Fetching data from source...')
    // this.convertTableService.convertTable({id:'customer_table'}).then((status)=>{
    //   console.log("----**** status", status)
    //   if(status){
    //     this.isCallable = false
    //     console.log("Not Callable")
    //   }
    // })
    const services = {'prepaidcustomers':{$:this.customerService.nextPage(link,'prepaid'),setter:this.customerService.swapCustomerlist},
                    'postpaidcustomers':{$:this.customerService.nextPage(link,'postpaid'),setter:this.customerService.swapCustomerlist}}
      services[cmp].$.subscribe((response)=>{
        // console.log(response)
        services[cmp]['setter'](response)
        const e = $event.target

      let links = this.getSiblings(e.parentElement)
      console.log(links)
      links.forEach((link)=>{
        link.classList.remove('active')
      })

      $event.target.parentElement.classList.add('active')
      })
    
  }

  loadMoreItems() {
    // call your function here to load more items
    if(this.isCallable){
      console.log('Loading more items...');
    const last = this.blocks[this.blocks.length - 1]
    if(last+403 < this.cap){
      console.log(last, last + 403)
      console.log(this.generateMultiplesOfThree(last+3,last+3 + 400))
      this.blocks =this.blocks.concat(this.generateMultiplesOfThree(last+3,last+3 + 400))
      console.log(this.blocks)
    }
    else{ //not working
      this.blocks =this.blocks.concat(this.generateMultiplesOfThree(last+3,last+3 + this.cap-last))
      this.blocks = this.removeElementsAfter(this.blocks,this.cap)
      console.log(this.blocks)
      this.isCallable = false
    }
    }
  }

  removeElementsAfter(array, element) {
    const index = array.indexOf(element);
    if (index !== -1) {
      array.splice(index + 1);
    }
    return array;
  }

  setPage(pageNumber: number) {
    this.paginationService.setPage(pageNumber);
    this.currentPage = this.paginationService.getCurrentPage();
  }

  loadMorePages() {
      const start = this.displayedPages.length;
      const end = start + 5;
      
      let newLinks = []
    if(!this.firstrun){
      this.currentPage += 5;
    }
    else{
      this.currentPage += 10;
    }
      
      for(let i=this.currentPage-6; i< this.currentPage-1; i++){
        newLinks.push({page:i+1,link:i+1,cmp:this.paginationService.getActiveCmp()})
      }
      [...this.links.splice(5,0, ...newLinks)]
      this.links.splice(0,5)
      console.log(this.currentPage)
      this.showLoadMoreButton = this.currentPage < this.totalPages;
      this.activateLessButton = true
    
    this.firstrun = false
    
  }

  backTrackPages() {
    
    let newLinks = []
  if(!this.firstrun){
    this.currentPage -= 5;
    for(let i=this.currentPage-5; i< this.currentPage; i++){
      newLinks.push({page:i,link:i,cmp:this.paginationService.getActiveCmp()})
    }
    console.log(...this.links.splice(5,0, ...newLinks))
    this.links.splice(0,5)
    this.showLoadMoreButton = this.currentPage < this.totalPages;
    this.activateLessButton = this.currentPage -5 > 1
  }
  this.firstrun = false
  
}
}
