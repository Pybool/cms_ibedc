import { Directive, ElementRef, HostListener } from '@angular/core';

@Directive({
  selector: '[appTitlecase]'
})
export class TitlecaseDirective {

  constructor(private el: ElementRef) { }

  @HostListener('input', ['$event.target.value'])
  onInput(value: string) {
    this.el.nativeElement.value = value.toLowerCase().split(' ').map(word => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    }).join(' ');
  }

}
