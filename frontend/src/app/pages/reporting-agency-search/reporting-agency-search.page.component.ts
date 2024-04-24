import {Component, OnInit, signal, Signal, ViewChild, WritableSignal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";
import {debounceTime, Subject, take} from "rxjs";

import {ProgressSpinnerModule} from "primeng/progressspinner";
import {DbStatusService} from "../../core/services/database_status_service";
import {FormsModule} from "@angular/forms";
import {TableModule} from "primeng/table";
import {InputTextModule} from "primeng/inputtext";
import {DropdownModule} from "primeng/dropdown";
import {Paginator, PaginatorModule} from "primeng/paginator";
import {NWCGUnit, NWCGUnitFilters} from "../../core/models/nwcg_units.interface";
import {NWCGUnitService} from "../../core/services/nwcg_unit_service";
import {ReportingAgencyService} from "../../core/services/reporting_agency_service";
import {ReportingAgency, ReportingAgencyFilters} from "../../core/models/reporting_agencies.interface";

@Component({
  selector: 'reporting-agency-search',
  standalone: true,
  imports: [
    CommonModule,
    ButtonModule,
    CardModule,
    TableModule,
    InputTextModule,
    DropdownModule,
    FormsModule,
    ProgressSpinnerModule,
    PaginatorModule
  ],
  templateUrl: './reporting-agency-search.page.component.html',
})
export class ReportingAgencySearchComponent implements OnInit {
  reportingAgencies$: WritableSignal<ReportingAgency[]> = signal([]);
  currentPage$: WritableSignal<number> = signal(1);
  rowsPerPage$: WritableSignal<number> = signal(10);
  totalSize$: WritableSignal<number> = signal(0);

  agencyCodeFilter$: WritableSignal<string | undefined> = signal(undefined);
  reportingUnitIdFilter$: WritableSignal<string | undefined> = signal(undefined);
  reportingUnitNameFilter$: WritableSignal<string | undefined> = signal(undefined);

  private filterChangeSubject = new Subject<void>();

  firstRowIndex = 0;
  lastRowIndex = 10;
  dataReady: boolean = false;

  @ViewChild('paginatorRef') paginator!: Paginator;

  constructor(
    private dbStatusService: DbStatusService,
    private reportingAgencyService: ReportingAgencyService
  ) {
    this.filterChangeSubject.pipe(debounceTime(2000)).subscribe(() => {
      this.firstRowIndex = 0;
      this.lastRowIndex = this.totalSize$() > this.rowsPerPage$() ? this.rowsPerPage$() : this.totalSize$();
      this.currentPage$.set(1);
      this.paginator.changePage(0);
      this.updateData();
    });
  }

  ngOnInit() {
    this.dbStatusService.getTableSizes()
      .pipe(take(1)).subscribe((res) => {
      this.totalSize$.set(res.total_size);
      this.updateData();
    });
  }

  updateData() {
    this.dataReady = false;
    const skip = (this.currentPage$() - 1) * this.rowsPerPage$();
    const fetchOnly = this.rowsPerPage$();
    const filters: ReportingAgencyFilters = {};
    if (!!this.agencyCodeFilter$()) {
      filters.agency_code = this.agencyCodeFilter$();
    }
    if (!!this.reportingUnitIdFilter$()) {
      filters.reporting_unit_id = this.reportingUnitIdFilter$();
    }
    if (!!this.reportingUnitNameFilter$()) {
      filters.reporting_unit_name = this.reportingUnitNameFilter$();
    }
    filters.skip = skip;
    filters.take = fetchOnly;

    this.reportingAgencyService
      .getReportingAgencies(filters)
      .pipe(take(1))
      .subscribe((res) => {
        this.reportingAgencies$.set(res.reporting_agencies);
        this.totalSize$.set(res.total_count);
        this.dataReady = true;
      });
  }


  onPageChange(event: any) {
    this.rowsPerPage$.set(event.rows);
    this.firstRowIndex = event.first;
    this.lastRowIndex = event.page + 1 !== event.pageCount ? this.firstRowIndex + this.rowsPerPage$() : this.totalSize$();
    this.currentPage$.set(event.page + 1);
    this.updateData();
  }


  onFilterChange(event: any, filter_changed: string) {
    if (filter_changed == 'agency_name') {
      this.agencyCodeFilter$.set(event);
    }
    if (filter_changed == 'wildland_role') {
      this.reportingUnitIdFilter$.set(event);
    }
    if (filter_changed == 'geographic_area_code') {
      this.reportingUnitNameFilter$.set(event);
    }
    this.filterChangeSubject.next();
  }
}
