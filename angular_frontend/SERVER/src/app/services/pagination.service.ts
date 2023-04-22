import { Injectable } from '@angular/core';
import { BehaviorSubject, of } from 'rxjs';

@Injectable()
export class PaginationService {
  private currentPage = 1;
  private totalPages = 1;
  private firstLink;
  private lastLink
  private links$:any = new BehaviorSubject<any>({});
  activecmp:string;

  constructor() {}

  setLinks(first,last,cmp){
    this.activecmp = cmp
    this.firstLink = first
    this.lastLink = last
    this.links$.next({links:this.generateLinks()}) 
    console.log(this.firstLink, this.lastLink)
  }

  getActiveCmp(){
    return this.activecmp
  }

  generateLinks$() {
    console.log("*****************************")
    return this.links$.asObservable()
  }

  generateLinks() {
    let links: Array<any> = [];
    console.log(this.firstLink, this.lastLink)
    const firstLinkPageNumber = 1//this.getPageNumberFromLink(this.firstLink);
    const lastLinkPageNumber = Math.round(this.getPageNumberFromLink(this.lastLink)/100);

    this.totalPages =  lastLinkPageNumber;
    console.log(firstLinkPageNumber, lastLinkPageNumber)

    // Add first five links
    for (let i = firstLinkPageNumber; i <= firstLinkPageNumber + 4 && i <= lastLinkPageNumber; i++) {
      links.push({ page: i, link: this.generateLink(i), cmp:this.activecmp });
    }
    console.log("First five ", links)

    // Add "More" link if necessary
    if (lastLinkPageNumber > firstLinkPageNumber + 4) {
      links.push({ page: null, link: 'More' });
    }

    // Add last five links
    for (let i = lastLinkPageNumber - 4; i <= lastLinkPageNumber; i++) {
      if (i >= firstLinkPageNumber && i > firstLinkPageNumber + 4) {
        links.push({ page: i, link: this.generateLink(i) , cmp:this.activecmp });
      }
    }

    return links;
  }

  private generateLink(pageNumber: number) {
    return pageNumber
  }

  private getPageNumberFromLink(url) {
    const urlSearchParams = new URLSearchParams(new URL(url).search);
    return parseInt(urlSearchParams.get("offset"));
  }

  setPage(pageNumber: number) {
    this.currentPage = pageNumber;
  }

  getCurrentPage() {
    return this.currentPage;
  }

  getTotalPages() {
    return this.totalPages;
  }
}



