import { Injectable } from '@angular/core';
import { ComponentRef, ComponentFactoryResolver, ApplicationRef, Injector } from '@angular/core';
import { SpinnerComponent } from '../ui/spinner/spinner.component';


@Injectable({
  providedIn: 'root'
})
export class SpinnerService {
  private spinnerRef: ComponentRef<SpinnerComponent>;

  constructor(
    private componentFactoryResolver: ComponentFactoryResolver,
    private appRef: ApplicationRef,
    private injector: Injector
  ) {}

  public showSpinner(parentElement: HTMLElement): void {
    console.log(parentElement)
    if (!this.spinnerRef) {
      // Create the spinner component if it doesn't exist
      const spinnerFactory = this.componentFactoryResolver.resolveComponentFactory(SpinnerComponent);
      this.spinnerRef = spinnerFactory.create(this.injector);
      this.appRef.attachView(this.spinnerRef.hostView);
      console.log("done attaching spinner ",this.spinnerRef.hostView)
    }

    // Add the spinner component to the parent element
    parentElement.appendChild(this.spinnerRef.location.nativeElement);
  }

  public hideSpinner(): void {
    if (this.spinnerRef) {
      // Remove the spinner component from the DOM
      this.appRef.detachView(this.spinnerRef.hostView);
      this.spinnerRef.destroy();
      this.spinnerRef = null;
    }
  }
}
