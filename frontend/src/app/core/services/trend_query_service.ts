import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters} from "../models/fire_incidents.interface";
import {
  AgencyContainmentTimeData,
  AgencyContainmentTimeFilters,
  WildFireChangesInSizeAndFrequency,
  SizeOfWildfireTypesData,
  SizeOfWildfireTypesFilters,
  WildFireChangesInSizeAndFrequencyFilters,
  wildfireSizeBasedOnGeoData,
  wildfireSizeBasedOnGeoFilters,
  WildfireTypesBasedOnGeoData,
  WildfireTypesBasedOnGeoFilters, UnitInformation, AgencyInformation
} from "../models/trend_query_dto.interface";


@Injectable({
  providedIn: 'root'
})
export class TrendQueryService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

  getWildFireSizeAndFrequency(filters: WildFireChangesInSizeAndFrequencyFilters): Observable<WildFireChangesInSizeAndFrequency[]> {
    return this.httpClient.post<WildFireChangesInSizeAndFrequency[]>(this.REST_API_SERVER + `/trends/changes-in-size-and-frequency`, filters).pipe(
      take(1),
      map((res: WildFireChangesInSizeAndFrequency[]) => {
        return res;
      })
    )
  }

  getWildFireTypesBasedOnGeo(filters: WildfireTypesBasedOnGeoFilters): Observable<WildfireTypesBasedOnGeoData[]> {
    return this.httpClient.post<WildfireTypesBasedOnGeoData[]>(this.REST_API_SERVER + `/trends/type-of-wildfire-geo`, filters).pipe(
      take(1),
      map((res: WildfireTypesBasedOnGeoData[]) => {
        return res;
      })
    )
  }

  getAgencyContainmentTime(filters: AgencyContainmentTimeFilters): Observable<AgencyContainmentTimeData[]> {
    return this.httpClient.post<AgencyContainmentTimeData[]>(this.REST_API_SERVER + `/trends/agency-containment-time`, filters).pipe(
      take(1),
      map((res: AgencyContainmentTimeData[]) => {
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

  getUnitInformation(): Observable<UnitInformation[]> {
    return this.httpClient.get<UnitInformation[]>(this.REST_API_SERVER + '/trends/unit_information').pipe(
      take(1),
      map((res: UnitInformation[]) => {
        return res;
      })
    )
  }

  getCauseDescriptions(): Observable<string[]> {
    return this.httpClient.get<string[]>(this.REST_API_SERVER + '/trends/cause_descriptions').pipe(
      take(1),
      map((res: string[]) => {
        return res;
      })
    )
  }

  getAgencyInformation(): Observable<AgencyInformation[]> {
    return this.httpClient.get<AgencyInformation[]>(this.REST_API_SERVER + '/trends/reporting_agencies').pipe(
      take(1),
      map((res: AgencyInformation[]) => {
        return res;
      })
    )
  }
}
