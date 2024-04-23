import {Component, OnInit, signal, Signal, ViewChild, WritableSignal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";
import {debounceTime, Subject, take} from "rxjs";

import {ProgressSpinnerModule} from "primeng/progressspinner";
import {FireIncidentsService} from "../../core/services/fire_incidents_service";
import {FireIncident, FireIncidentFilters} from "../../core/models/fire_incidents.interface";
import {DbStatusService} from "../../core/services/database_status_service";
import {FormsModule} from "@angular/forms";
import {TableModule} from "primeng/table";
import {InputTextModule} from "primeng/inputtext";
import {DropdownModule} from "primeng/dropdown";
import {Paginator, PaginatorModule} from "primeng/paginator";

@Component({
  selector: 'fire-incident-search',
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
  templateUrl: './fire-incident-search.page.component.html',
})
export class FireIncidentSearchComponent implements OnInit {
  fireIncidents$: WritableSignal<FireIncident[]> = signal([]);
  currentPage$: WritableSignal<number> = signal(1);
  rowsPerPage$: WritableSignal<number> = signal(10);
  totalSize$: WritableSignal<number> = signal(0);

  sizeCategoryFilter$: WritableSignal<string | undefined> = signal(undefined);
  yearOfFireMinFilter$: WritableSignal<number | undefined> = signal(undefined);
  yearOfFireMaxFilter$: WritableSignal<number | undefined> = signal(undefined);

  private filterChangeSubject = new Subject<void>();

  firstRowIndex = 0;
  lastRowIndex = 10;
  dataReady: boolean = false;

  @ViewChild('paginatorRef') paginator!: Paginator;

  constructor(
    private dbStatusService: DbStatusService,
    private fireIncidentService: FireIncidentsService
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
    const filters: FireIncidentFilters = {};
    if (!!this.sizeCategoryFilter$()) {
      filters.size_category = this.sizeCategoryFilter$();
    }
    if (!!this.yearOfFireMinFilter$()) {
      filters.year_of_fire_min = this.yearOfFireMinFilter$();
    }
    if (!!this.yearOfFireMaxFilter$()) {
      filters.year_of_fire_min = this.yearOfFireMaxFilter$();
    }
    filters.skip = skip;
    filters.take = fetchOnly;

    this.fireIncidentService
      .getFireIncidents(filters)
      .pipe(take(1))
      .subscribe((res) => {
        this.fireIncidents$.set(res.fire_incidents);
        this.totalSize$.set(res.total_count);
        this.dataReady = true;
      });
  }

  onPageChange(event: any) {
    this.firstRowIndex = event.first;
    this.lastRowIndex = event.page + 1 !== event.pageCount ? this.firstRowIndex + this.rowsPerPage$() : this.totalSize$();
    this.currentPage$.set(event.page + 1);
    this.updateData();
  }

  onRowsPerPageChange(event: any) {
    this.rowsPerPage$.set(event.value);
    this.updateData();
  }


  onFilterChange(event: any, filter_changed: string) {
    if (filter_changed == 'size_category') {
      this.sizeCategoryFilter$.set(event);
    }
    if (filter_changed == 'year_of_fire_min') {
      this.yearOfFireMinFilter$.set(event);
    }
    if (filter_changed == 'year_of_fire_max') {
      this.yearOfFireMaxFilter$.set(event);
    }
    this.filterChangeSubject.next();
  }
}
