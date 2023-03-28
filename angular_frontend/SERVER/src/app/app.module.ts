import { EdituserModule } from './pages/user/edituser/edituser.module';
import { UserEffects } from './pages/user/users/state/user.effects';
import { DecimalPipe } from '@angular/common';
import { BootstrapOptions, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { EffectsModule } from '@ngrx/effects';
import { MetaReducer, StoreModule } from '@ngrx/store';
import { AuthEffects } from './authentication/state/auth.effects'
import { reducers } from './basestore/app.states';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { CustomersComponent } from './pages/customersmodule/prepaidcustomers/customers.component';
import { LoginComponent } from './authentication/login/login.component';
import { ResetpasswordComponent } from './authentication/resetpassword/resetpassword.component';
import { AuthService } from './services/auth.service';
import { environment } from 'src/environments/environment.prod';
import { CustomercreationComponent } from './pages/customercreation/customercreation.component';
import { CustomerupdateComponent } from './pages/customerupdate/customerupdate.component';
import { ApprovalboardComponent } from './pages/approvalboard/approvalboard.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UsersComponent } from './pages/user/users/users.component';
import { LocationsComponent } from './pages/locations/locations.component';
import { ConfigurationsComponent } from './pages/configurations/configurations.component';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'; 
import { localStorageReducer } from './basestore/app.reducer';
import { TitlecaseDirective } from './directives/titlecase.directive';
import { CustomSelectEffects } from './ui/customselect/state/customselect.effects';
import { CreateUserEffects } from './pages/user/state/createuser.effects';
import { CreateuserModule } from './pages/user/createuser/createuser.module';
import {DataTablesModule} from 'angular-datatables';
import { CustomerEffects } from './pages/customersmodule/prepaidcustomers/state/customer.effects';
import { TitleCasePipe } from './pipes/titlecase.pipe';
import { ConfigurationsModule } from './pages/configurations/configurations.module';
import { CustomerCreationEffects } from './pages/customercreation/state/customercreation.effects';
import { CustomercreationModule } from './pages/customercreation/customercreation.module';
import { CrmdComponent } from './pages/crmd/crmd.component';
import { CaadlistComponent } from './pages/caadlist/caadlist.component';
import { CustomerCaadEffects } from './pages/customerdetails/caad/state/customercaad.effects';
import { CaadListEffects } from './pages/caadlist/state/caadlist.effects';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { DynamicScriptDirective } from './directives/dynamic-script.directive';
import { SpinnerComponent } from './ui/spinner/spinner.component';
import { PostpaidcustomersComponent } from './pages/customersmodule/postpaidcustomers/postpaidcustomers.component';
import { BillingComponent } from './pages/billing/billing.component';
import { PaymentsComponent } from './pages/payments/payments.component';
import { EmsCustomerEffects } from './pages/customersmodule/postpaidcustomers/state/customer.effects';
import { PaymentsemsComponent } from './pages/paymentsems/paymentsems.component';
import { TodaycollectionsecmiComponent } from './pages/todaycollectionsecmi/todaycollectionsecmi.component';
import { TodaycollectionsemsComponent } from './pages/todaycollectionsems/todaycollectionsems.component';
import { NotificationmodalComponent } from './ui/notificationmodal/notificationmodal.component';
import { LocationsEffects } from './pages/locations/state/location.effects';


const metaReducers: Array<MetaReducer<any, any>> = [localStorageReducer];

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    CustomersComponent,
    TitleCasePipe,
    LoginComponent,
    ResetpasswordComponent,
    CustomercreationComponent,
    CustomerupdateComponent,
    ApprovalboardComponent,
    UsersComponent,
    LocationsComponent,
    ConfigurationsComponent,
    TitlecaseDirective,
    CrmdComponent,
    CaadlistComponent,
    DynamicScriptDirective,
    SpinnerComponent,
    PostpaidcustomersComponent,
    BillingComponent,
    PaymentsComponent,
    PaymentsemsComponent,
    TodaycollectionsecmiComponent,
    TodaycollectionsemsComponent,
    NotificationmodalComponent
    
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    AppRoutingModule,
    HttpClientModule,
    MatTableModule,
    MatSortModule,
    MatPaginatorModule,
    StoreModule.forRoot(reducers, {  }),
    EffectsModule.forRoot([AuthEffects,CustomSelectEffects,CreateUserEffects,
                           UserEffects,CustomerEffects,CustomerCreationEffects,
                           CustomerCaadEffects,CaadListEffects,EmsCustomerEffects,
                           LocationsEffects]),
    ToastrModule.forRoot({positionClass: 'toast-top-center',
    preventDuplicates: true,autoDismiss:false}),
    StoreDevtoolsModule.instrument({
      logOnly: environment.production,
    }),
    ReactiveFormsModule,
    FormsModule,
    EdituserModule,
    CreateuserModule,
    ConfigurationsModule,
    DataTablesModule,
    // CustomercreationModule
  ],
  
  providers: [AuthService,DecimalPipe,

    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
],
  bootstrap: [AppComponent],
})
export class AppModule { }
