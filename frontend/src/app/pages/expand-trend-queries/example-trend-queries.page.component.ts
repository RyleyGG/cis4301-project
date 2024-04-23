import {Component, OnInit, signal, Signal, WritableSignal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";
import {take} from "rxjs";

import {DbStatusService} from "../../core/services/database_status_service";
import {ProgressSpinnerModule} from "primeng/progressspinner";

@Component({
  selector: 'app-example-trend-queries',
  standalone: true,
  imports: [CommonModule, ButtonModule, RouterLink, CardModule, ProgressSpinnerModule],
  templateUrl: './example-trend-queries.page.component.html',
})
export class ExampleTrendQueriesComponent implements OnInit {

  constructor(private dbStatusService: DbStatusService) {
  }

  ngOnInit() {
  }
}
