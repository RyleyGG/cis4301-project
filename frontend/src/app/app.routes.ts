import {Routes} from '@angular/router';
import {AppComponent} from './app.component';
import {LandingPageComponent} from './pages/landing/landing.page.component';

export const routes: Routes = [
  // General
  {path: "landing", component: LandingPageComponent},
  {path: '', redirectTo: '/landing', pathMatch: 'full'},
  {path: '**', component: AppComponent} // TODO: make this a PageNotFound or 404 error page
];
