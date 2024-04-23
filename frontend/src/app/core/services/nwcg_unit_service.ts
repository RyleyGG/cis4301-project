import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters, FireIncidentSearch} from "../models/fire_incidents.interface";
import {NWCGUnitFilters, NWCGUnitSearch} from "../models/nwcg_units.interface";

@Injectable({
  providedIn: 'root'
})
export class NWCGUnitService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

  getNWCGUnits(filters: NWCGUnitFilters): Observable<NWCGUnitSearch> {
    return this.httpClient.post<NWCGUnitSearch>(this.REST_API_SERVER + `/nwcg_units/search`, filters).pipe(
      take(1),
      map((res: NWCGUnitSearch) => {
        return res;
      })
    )
  }

}
