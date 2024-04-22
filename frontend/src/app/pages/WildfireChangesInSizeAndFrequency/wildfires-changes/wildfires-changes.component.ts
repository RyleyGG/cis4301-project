import { FormsModule } from '@angular/forms';
import { CalendarModule } from 'primeng/calendar';
import { ChartModule } from 'primeng/chart';
import { HttpClient } from '@angular/common/http';
import {Component, OnInit, signal, Signal, WritableSignal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";
import {take} from "rxjs";

import { TrendQueryService } from '../../../core/services/trend_query_service';

import {ProgressSpinnerModule} from "primeng/progressspinner";
import { WildFireChangesInSizeAndFrequencyFilters } from '../../../core/models/trend_query_dto.interface';




@Component({
  selector: 'app-wildfires-changes',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule],
  templateUrl: './wildfires-changes.component.html',
  styleUrl: './wildfires-changes.component.css'
})

export class WildfireChangesInSizeAndFrequencyComponent {
  startDate: Date = new Date();  // Date property for calendar binding
  endDate: Date = new Date();  // Date property for calendar binding

  chartLabels$: WritableSignal<string[]> = signal([]);
  chartDatasets$: WritableSignal<any[]> = signal([]);

  data: any;
  options: any;

  constructor(private http: HttpClient, private trendQueryService: TrendQueryService) {
    // this.initializeChartData();
  }

  initializeChartData() {
    this.data = {
      labels: this.chartLabels$(),
      datasets: this.chartDatasets$()
    };
    this.options = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      }
    };
  }

  submitSizeAndFrequencyForm() {
      const formData: WildFireChangesInSizeAndFrequencyFilters = {
        start_date: this.startDate,
        end_date: this.endDate,
      };
  

    // TODO: define signals and integrate into API requests
    this.trendQueryService.getWildFireSizeAndFrequency(formData)
      .pipe((take(1)))
      .subscribe((res) => {
        console.log(res);

        // TODO: integrate live result data into signal computation
        this.chartLabels$.set(['2000', '2001', '2002', '2003', '2004', '2005', '2006']);
        this.chartDatasets$.set([
          {
            label: 'Demo Data',
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: '#42A5F5'
          }
        ]);

        this.initializeChartData();
      });
  }
}