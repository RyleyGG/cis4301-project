import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";
import {FireIncident, FireIncidentFilters, FireIncidentSearch} from "../models/fire_incidents.interface";

@Injectable({
  providedIn: 'root'
})
export class FireIncidentsService {
  private REST_API_SERVER = "http://localhost:8000";

  constructor(private httpClient: HttpClient) {

  }

  getFireIncidents(filters: FireIncidentFilters): Observable<FireIncidentSearch> {
    return this.httpClient.post<FireIncidentSearch>(this.REST_API_SERVER + `/fire_incidents/search`, filters).pipe(
      take(1),
      map((res: FireIncidentSearch) => {
        return res;
      })
    )
  }

}
