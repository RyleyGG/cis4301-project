import {Component, OnInit, signal, Signal, WritableSignal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";
import {take} from "rxjs";

import {DbStatusService} from "../../core/services/database_status_service";
import {ProgressSpinnerModule} from "primeng/progressspinner";

@Component({
  selector: 'database-status',
  standalone: true,
  imports: [CommonModule, ButtonModule, RouterLink, CardModule, ProgressSpinnerModule],
  templateUrl: './database-status.page.component.html',
})
export class DatabaseStatusComponent implements OnInit {
  fireIncidentSize$: WritableSignal<number> = signal(0);
  nwcgUnitSize$: WritableSignal<number> = signal(0);
  reportingAgencySize$: WritableSignal<number> = signal(0);
  totalSize$: WritableSignal<number> = signal(0);
  dataReady: boolean = false;

  constructor(private dbStatusService: DbStatusService) {
  }

  ngOnInit() {
    this.dbStatusService.getTableSizes().pipe(take(1)).subscribe((res) => {
      this.fireIncidentSize$.set(res.fire_incident_size);
      this.nwcgUnitSize$.set(res.nwcg_unit_size);
      this.reportingAgencySize$.set(res.reporting_agency_size);
      this.totalSize$.set(res.total_size);
      this.dataReady = true;
    })
  }
}
