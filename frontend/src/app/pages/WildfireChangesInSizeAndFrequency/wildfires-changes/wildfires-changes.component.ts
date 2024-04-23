import {Component, OnInit, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CalendarModule} from 'primeng/calendar';
import {ChartModule} from 'primeng/chart';
import {TrendQueryService} from '../../../core/services/trend_query_service';
import {WildFireChangesInSizeAndFrequencyFilters} from '../../../core/models/trend_query_dto.interface';
import {take} from 'rxjs/operators';
import {InputTextModule} from "primeng/inputtext";
import {debounceTime, Subject} from "rxjs";

@Component({
  selector: 'app-wildfires-changes',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule, InputTextModule],
  templateUrl: './wildfires-changes.component.html',
  styleUrls: ['./wildfires-changes.component.css']
})
export class WildfireChangesInSizeAndFrequencyComponent implements OnInit {
  startDate$: WritableSignal<number | undefined> = signal(undefined);
  endDate$: WritableSignal<number | undefined> = signal(undefined);
  chartLabels$: WritableSignal<string[]> = signal([]);
  avgFireSizeDataset$: WritableSignal<any[]> = signal([]);
  totalFireSizeDataset$: WritableSignal<any[]> = signal([]);
  totalFireNumDataset$: WritableSignal<any[]> = signal([]);
  avgFireSizeData: any;
  totalFireSizeData: any;
  totalFireNumData: any;
  options: any;

  dataReady = false;

  constructor(private trendQueryService: TrendQueryService) {
  }

  ngOnInit() {
    this.initializeChartData();
    this.dataReady = true;
  }

  initializeChartData() {
    this.avgFireSizeData = {labels: this.chartLabels$(), datasets: this.avgFireSizeDataset$()};
    this.totalFireSizeData = {labels: this.chartLabels$(), datasets: this.totalFireSizeDataset$()};
    this.totalFireNumData = {labels: this.chartLabels$(), datasets: this.totalFireNumDataset$()};
    this.options = {
      responsive: true,
      plugins: {
        legend: {display: true, position: 'top'}
      }
    };
  }

  submitSizeAndFrequencyForm() {
    this.dataReady = false;
    const formData: WildFireChangesInSizeAndFrequencyFilters = {
      start_date: this.startDate$(),
      end_date: this.endDate$(),
    };

    console.log(formData);
    this.trendQueryService.getWildFireSizeAndFrequency(formData)
      .pipe(take(1))
      .subscribe((res) => {
        // set labels
        this.chartLabels$.set(res.map((resObj) => {
          return resObj.year_of_fire.toString();
        }));

        // set datasets
        // there should be a line each for avg fire size, total fires size, total number of fires
        const avg_fire_size_data = res.map((resObj) => resObj.avg_fire_size);
        const total_fires_size_data = res.map((resObj) => resObj.total_fires_size);
        const total_number_of_fires_data = res.map((resObj) => resObj.total_number_of_fires);
        this.avgFireSizeDataset$.set(
          [
            {
              label: 'Average Fire Size',
              data: avg_fire_size_data,
              fill: false,
              tension: 0.4
            }
          ]
        )
        this.totalFireSizeDataset$.set(
          [
            {
              label: 'Total Fires Size',
              data: total_fires_size_data,
              fill: false,
              tension: 0.4
            }
          ]
        )
        this.totalFireNumDataset$.set(
          [
            {
              label: 'Total Number of Fires',
              data: total_number_of_fires_data,
              fill: false,
              tension: 0.4
            }
          ]
        )

        this.initializeChartData();
        this.dataReady = true;
      });
  }

}
