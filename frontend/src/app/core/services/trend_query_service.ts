import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters} from "../models/fire_incidents.interface";
import {wildfireSizeBasedOnGeoData, wildfireSizeBasedOnGeoFilters} from "../models/trend_query_dto.interface";

@Injectable({
  providedIn: 'root'
})
export class TrendQueryService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

  getWildFireSizeBasedOnGeo(filters: wildfireSizeBasedOnGeoFilters): Observable<wildfireSizeBasedOnGeoData> {
    return this.httpClient.post<wildfireSizeBasedOnGeoData>(this.REST_API_SERVER + `/dummy/size-of-wildfire-based-on-geographic-area-form-submission`, filters).pipe(
      take(1),
      map((res: wildfireSizeBasedOnGeoData) => {
        return res;
      })
    )
  }
}
