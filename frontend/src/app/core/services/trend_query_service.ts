import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters} from "../models/fire_incidents.interface";
import {AgencyContaintmentTimeData, AgencyContaintmentTimeFilters, WildFireChangesInSizeAndFrequency, SizeOfWildfireTypesData ,SizeOfWildfireTypesFilters, WildFireChangesInSizeAndFrequencyFilters, wildfireSizeBasedOnGeoData, wildfireSizeBasedOnGeoFilters, WildfireTypesBasedOnGeoData, WildfireTypesBasedOnGeoFilters} from "../models/trend_query_dto.interface";


@Injectable({
  providedIn: 'root'
})
export class TrendQueryService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

getWildFireSizeAndFrequency(filters: WildFireChangesInSizeAndFrequencyFilters): Observable<WildFireChangesInSizeAndFrequency> {
  console.log("WORKING");
  return this.httpClient.post<WildFireChangesInSizeAndFrequency>(this.REST_API_SERVER + `/trends/changes-in-size-and-frequency-form-submission`, filters).pipe(
    take(1),
    map((res: WildFireChangesInSizeAndFrequency) => {
      return res;
    })
  )
}

getWildFireTypesBasedOnGeo(filters: WildfireTypesBasedOnGeoFilters): Observable<WildfireTypesBasedOnGeoData> {
  return this.httpClient.post<WildfireTypesBasedOnGeoData>(this.REST_API_SERVER + `/trends/type-of-wildfire-form-submission`, filters).pipe(
    take(1),
    map((res: WildfireTypesBasedOnGeoData) => {
      return res;
    })
  )
}

getAgencyContainmentTime(filters: AgencyContaintmentTimeFilters): Observable<AgencyContaintmentTimeData> {
  return this.httpClient.post<AgencyContaintmentTimeData>(this.REST_API_SERVER + `/trends/agency-containment-time-form`, filters).pipe(
    take(1),
    map((res: AgencyContaintmentTimeData) => {
      return res;
    })
  )
}

getSizeOfWildFireTypes(filters: SizeOfWildfireTypesFilters): Observable<SizeOfWildfireTypesData> {
  return this.httpClient.post<SizeOfWildfireTypesData>(this.REST_API_SERVER + `/trends/size-of-wildfire-types-form-submission`, filters).pipe(
    take(1),
    map((res: SizeOfWildfireTypesData) => {
      return res;
    })
  )
}
  getWildFireSizeBasedOnGeo(filters: wildfireSizeBasedOnGeoFilters): Observable<wildfireSizeBasedOnGeoData> {
    return this.httpClient.post<wildfireSizeBasedOnGeoData>(this.REST_API_SERVER + `/trends/size-of-wildfire-based-on-geographic-area-form-submission`, filters).pipe(
      take(1),
      map((res: wildfireSizeBasedOnGeoData) => {
        return res;
      })
    )
  }

  
}