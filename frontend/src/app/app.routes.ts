import {Routes} from '@angular/router';
import {AppComponent} from './app.component';
import {LandingPageComponent} from './pages/landing/landing.page.component';
import {
  WildfireChangesInSizeAndFrequencyComponent
} from './pages/WildfireChangesInSizeAndFrequency/wildfires-changes/wildfires-changes.component';
import {
  wildfireTypesBasedOnGeographyComponent
} from './pages/wildfire-types-based-on-geography/wildfire-types-based-on-geography.component';
import {
  WildfireSizesBasedOnGeographyComponent
} from './pages/wildfire-sizes-based-on-geography/wildfire-sizes-based-on-geography.component';
import {AgencyContaintmentTimeComponent} from './pages/agency-containment-time/agency-containment-time.component';
import {DatabaseStatusComponent} from "./pages/db-status/database-status.page.component";
import {SizeOfWildfireTypesComponent} from './pages/size-of-wildfire-types/size-of-wildfire-types.component';
import {FireIncidentSearchComponent} from "./pages/fire-incident-search/fire-incident-search.page.component";
import {NWCGUnitSearchComponent} from "./pages/nwcg-unit-search/nwcg-unit-search.page.component";


export const routes: Routes = [
  // General
  {path: "landing", component: LandingPageComponent},
  {path: '', redirectTo: '/landing', pathMatch: 'full'},
  {path: "wildfire-changes-in-size-and-frequency", component: WildfireChangesInSizeAndFrequencyComponent},
  {path: "wildfire-sizes-geography", component: WildfireSizesBasedOnGeographyComponent},
  {path: "wildfire-types-geography", component: wildfireTypesBasedOnGeographyComponent},
  {path: "containment-vs-size", component: AgencyContaintmentTimeComponent},
  {path: "wildfire-types-size", component: SizeOfWildfireTypesComponent},
  {path: "status", component: DatabaseStatusComponent},
  {path: "fire-incident-search", component: FireIncidentSearchComponent},
  {path: "nwcg-unit-search", component: NWCGUnitSearchComponent},
  {path: '**', component: AppComponent} // TODO: make this a PageNotFound or 404 error page
];
