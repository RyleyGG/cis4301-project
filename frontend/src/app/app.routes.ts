import {Routes} from '@angular/router';
import {AppComponent} from './app.component';
import {LandingPageComponent} from './pages/landing/landing.page.component';
import {
  WildfiresChangesComponent
} from './pages/WildfireChangesInSizeAndFrequency/wildfires-changes/wildfires-changes.component';
import {
  WildfireTypesBasedOnGeographyComponent
} from './pages/wildfire-types-based-on-geography/wildfire-types-based-on-geography.component';
import {
  WildfireSizesBasedOnGeographyComponent
} from './pages/wildfire-sizes-based-on-geography/wildfire-sizes-based-on-geography.component';
import {AgencyContainmentTimeComponent} from './pages/agency-containment-time/agency-containment-time.component';
import {SizeOfWildfireTypesComponent} from './pages/size-of-wildfire-types/size-of-wildfire-types.component';
import {DatabaseStatusComponent} from "./pages/db-status/database-status.page.component";
import {FireIncidentSearchComponent} from "./pages/fire-incident-search/fire-incident-search.page.component";


export const routes: Routes = [
  // General
  {path: "landing", component: LandingPageComponent},
  {path: '', redirectTo: '/landing', pathMatch: 'full'},
  {path: "wildfire-changes-in-size-and-frequency", component: WildfiresChangesComponent},
  {path: "wildfire-sizes-geography", component: WildfireSizesBasedOnGeographyComponent},
  {path: "wildfire-types-geography", component: WildfireTypesBasedOnGeographyComponent},
  {path: "containment-vs-size", component: AgencyContainmentTimeComponent},
  {path: "wildfire-types-size", component: SizeOfWildfireTypesComponent},
  {path: "status", component: DatabaseStatusComponent},
  {path: "fire-incident-search", component: FireIncidentSearchComponent},
  {path: '**', component: AppComponent} // TODO: make this a PageNotFound or 404 error page
];
