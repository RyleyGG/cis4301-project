import {Injectable} from "@angular/core";
import {map, Observable, take} from "rxjs";
import {TblSizeResp} from "../models/db_status.interface";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class DbStatusService {
  private REST_API_SERVER = "http://localhost:8000/";

  constructor(private httpClient: HttpClient) {

  }

  getTableSizes(): Observable<TblSizeResp> {
    return this.httpClient.get<TblSizeResp>(this.REST_API_SERVER + `db_status`).pipe(
      take(1),
      map((res: TblSizeResp) => {
        return res;
      })
    )
  }

}
