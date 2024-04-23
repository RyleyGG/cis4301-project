import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters, FireIncidentSearch} from "../models/fire_incidents.interface";
import {NWCGUnitFilters, NWCGUnitSearch} from "../models/nwcg_units.interface";
import {ReportingAgencyFilters, ReportingAgencySearch} from "../models/reporting_agencies.interface";

@Injectable({
  providedIn: 'root'
})
export class ReportingAgencyService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

  getReportingAgencies(filters: ReportingAgencyFilters): Observable<ReportingAgencySearch> {
    return this.httpClient.post<ReportingAgencySearch>(this.REST_API_SERVER + `/reporting_agencies/search`, filters).pipe(
      take(1),
      map((res: ReportingAgencySearch) => {
        return res;
      })
    )
  }

}
