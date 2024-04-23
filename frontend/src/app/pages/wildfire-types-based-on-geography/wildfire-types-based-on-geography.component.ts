import {Component, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CalendarModule} from 'primeng/calendar';
import {ChartModule} from 'primeng/chart';
import {HttpClient} from '@angular/common/http';
import {wildfireSizeBasedOnGeoFilters, WildfireTypesBasedOnGeoFilters} from "../../core/models/trend_query_dto.interface";
import {TrendQueryService} from "../../core/services/trend_query_service";
import {take} from "rxjs";  // Make sure to import HttpClient


@Component({
  selector: 'app-wildfire-types-based-on-geography',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule],  // Include FormsModule here
  templateUrl: './wildfire-types-based-on-geography.component.html',
  styleUrls: ['./wildfire-types-based-on-geography.component.css']  // Corrected property name and syntax
})

export class wildfireTypesBasedOnGeographyComponent {
  startDate: Date = new Date();  // Date property for calendar binding
  endDate: Date = new Date();  // Date property for calendar binding
  geographicArea: string = '';
  wildfireType: string = '';

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


  submitTypesForm() {
    const formData: WildfireTypesBasedOnGeoFilters = {
      start_date: this.startDate,
      end_date: this.endDate,
      geographic_area: this.geographicArea,
      wildfire_type: this.wildfireType
    };

    // TODO: define signals and integrate into API requests
    this.trendQueryService.getWildFireTypesBasedOnGeo(formData)
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
