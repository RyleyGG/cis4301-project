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

@Component({
  selector: 'nwcg-unit-search',
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
  templateUrl: './nwcg-unit-search.page.component.html',
})
export class NWCGUnitSearchComponent implements OnInit {
  nwcgUnits$: WritableSignal<NWCGUnit[]> = signal([]);
  currentPage$: WritableSignal<number> = signal(1);
  rowsPerPage$: WritableSignal<number> = signal(10);
  totalSize$: WritableSignal<number> = signal(0);

  agencyNameFilter$: WritableSignal<string | undefined> = signal(undefined);
  wildlandRoleFilter$: WritableSignal<string | undefined> = signal(undefined);
  geographicAreaCode$: WritableSignal<string | undefined> = signal(undefined);

  private filterChangeSubject = new Subject<void>();

  firstRowIndex = 0;
  lastRowIndex = 10;
  dataReady: boolean = false;

  @ViewChild('paginatorRef') paginator!: Paginator;

  constructor(
    private dbStatusService: DbStatusService,
    private nwcgUnitService: NWCGUnitService
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
    const filters: NWCGUnitFilters = {};
    if (!!this.agencyNameFilter$()) {
      filters.agency_name = this.agencyNameFilter$();
    }
    if (!!this.wildlandRoleFilter$()) {
      filters.wildland_role = this.wildlandRoleFilter$();
    }
    if (!!this.geographicAreaCode$()) {
      filters.geographic_area_code = this.geographicAreaCode$();
    }
    filters.skip = skip;
    filters.take = fetchOnly;

    this.nwcgUnitService
      .getNWCGUnits(filters)
      .pipe(take(1))
      .subscribe((res) => {
        this.nwcgUnits$.set(res.nwcg_units);
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
      this.agencyNameFilter$.set(event);
    }
    if (filter_changed == 'wildland_role') {
      this.wildlandRoleFilter$.set(event);
    }
    if (filter_changed == 'geographic_area_code') {
      this.geographicAreaCode$.set(event);
    }
    this.filterChangeSubject.next();
  }
}
