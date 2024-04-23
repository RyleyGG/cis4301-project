import {Component, OnInit, signal, WritableSignal} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CalendarModule } from 'primeng/calendar';
import { ChartModule } from 'primeng/chart';
import { TrendQueryService } from '../../../core/services/trend_query_service';
import { WildFireChangesInSizeAndFrequencyFilters } from '../../../core/models/trend_query_dto.interface';
import { take } from 'rxjs/operators';

@Component({
  selector: 'app-wildfires-changes',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule],
  templateUrl: './wildfires-changes.component.html',
  styleUrls: ['./wildfires-changes.component.css']
})
export class WildfireChangesInSizeAndFrequencyComponent implements OnInit {
  startDate: Date = new Date();
  endDate: Date = new Date();
  chartLabels$: WritableSignal<string[]> = signal([]);
  chartDatasets$: WritableSignal<any[]> = signal([]);
  data: any;
  options: any;

  constructor(private trendQueryService: TrendQueryService) {}

  ngOnInit() {
    this.initializeChartData();
  }

  initializeChartData() {
    this.data = { labels: this.chartLabels$(), datasets: this.chartDatasets$() };
    this.options = {
      responsive: true,
      plugins: {
        legend: { display: true, position: 'top' }
      }
    };
  }

  submitSizeAndFrequencyForm() {
    const formData: WildFireChangesInSizeAndFrequencyFilters = {
      start_date: this.startDate,
      end_date: this.endDate,
    };
    console.log(formData);
  
    this.trendQueryService.getWildFireSizeAndFrequency(formData)
      .pipe(take(1))
      .subscribe({
        next: (res) => {
          // Process the response and update chart data
        },
        error: (error) => {
          console.error('Error fetching data:', error);
        }
      });
  }
  
}
