import { Injectable } from '@angular/core';

@Injectable()
export class PaginationService {
  private currentPage = 1;
  private totalPages = 1;

  constructor() {}

  generateLinks(firstLink: string, lastLink: string) {
    let links: Array<any> = [];
    const firstLinkPageNumber = this.getPageNumberFromLink(firstLink);
    const lastLinkPageNumber = this.getPageNumberFromLink(lastLink);

    this.totalPages = lastLinkPageNumber;

    // Add first five links
    for (let i = firstLinkPageNumber; i <= firstLinkPageNumber + 4 && i <= lastLinkPageNumber; i++) {
      links.push({ page: i, link: this.generateLink(i) });
    }

    // Add "More" link if necessary
    if (lastLinkPageNumber > firstLinkPageNumber + 4) {
      links.push({ page: null, link: 'More' });
    }

    // Add last five links
    for (let i = lastLinkPageNumber - 4; i <= lastLinkPageNumber; i++) {
      if (i >= firstLinkPageNumber && i > firstLinkPageNumber + 4) {
        links.push({ page: i, link: this.generateLink(i) });
      }
    }

    return links;
  }

  private generateLink(pageNumber: number) {
    return `/page/${pageNumber}`;
  }

  private getPageNumberFromLink(link: string) {
    const match = link.match(/page\/(\d+)/);
    return match ? parseInt(match[1]) : 1;
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



import { Component } from '@angular/core';
// import { PaginationService } from './pagination.service';

@Component({
  selector: 'app-pagination',
  template: `
    <ul>
      <li *ngFor="let link of links">
        <a *ngIf="link.page" [routerLink]="link.link" [class.active]="link.page === currentPage">{{ link.page }}</a>
        <span *ngIf="!link.page">{{ link.link }}</span>
      </li>
    </ul>
  `,
})
export class PaginationComponent {
  links: Array<any>;
  currentPage: number;
  totalPages: number;

  constructor(private paginationService: PaginationService) {}

  ngOnInit() {
    const firstLink = 'https://example.com/api?page=1';
    const lastLink = 'https://example.com/api?page=10';

    this.links = this.paginationService.generateLinks(firstLink, lastLink);
    this.currentPage = this.paginationService.getCurrentPage();
    this.totalPages = this.paginationService.getTotalPages();
  }

  setPage(pageNumber: number) {
    this.paginationService.setPage(pageNumber);
    this.currentPage = this.paginationService.getCurrentPage();
  }
}
