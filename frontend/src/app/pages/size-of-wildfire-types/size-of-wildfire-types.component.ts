import {Component, OnInit, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CalendarModule} from 'primeng/calendar';
import {ChartModule} from 'primeng/chart';
import {HttpClient} from '@angular/common/http';
import {
  wildfireSizeBasedOnGeoFilters, WildfireTypesBasedOnGeoData,
  WildfireTypesBasedOnGeoFilters
} from "../../core/models/trend_query_dto.interface";
import {TrendQueryService} from "../../core/services/trend_query_service";
import {forkJoin, take} from "rxjs";
import {InputTextModule} from "primeng/inputtext";
import {DropdownModule} from "primeng/dropdown";
import {MultiSelectModule} from "primeng/multiselect";  // Make sure to import HttpClient


@Component({
  selector: "app-size-of-wildfire-types",
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule, InputTextModule, DropdownModule, MultiSelectModule],  // Include FormsModule here
  templateUrl: "./size-of-wildfire-types.component.html",
  styleUrl: "./size-of-wildfire-types.component.css",
})

export class SizeOfWildfireTypesComponent implements OnInit {
  startDate$: WritableSignal<number | undefined> = signal(undefined);
  endDate$: WritableSignal<number | undefined> = signal(undefined);
  geographicArea$: WritableSignal<any | undefined> = signal(undefined);
  causeDescription$: WritableSignal<any | undefined> = signal(undefined);

  chartLabels$: WritableSignal<string[]> = signal([]);

  avgFireSizeData: any;
  totalFireSizeData: any;
  totalFireNumData: any;
  avgFireSizeDataset$: WritableSignal<any[]> = signal([]);
  totalFireSizeDataset$: WritableSignal<any[]> = signal([]);
  totalFireNumDataset$: WritableSignal<any[]> = signal([]);

  avgFireSizeOpts: any;
  totalFireSizeOpts: any;
  dataReady = false;

  geographicAreaOpts: any = [];

  wildfireTypeOpts: any = [];

  constructor(private http: HttpClient, private trendQueryService: TrendQueryService) {
  }


  ngOnInit() {
    forkJoin([
      this.trendQueryService.getUnitInformation().pipe(take(1)),
      this.trendQueryService.getCauseDescriptions().pipe(take(1))
    ]).subscribe(([unitInfoRes, causeDescRes]) => {
      unitInfoRes.map((obj) => {
        this.geographicAreaOpts.push({name: obj.unit_name, code: obj.geographic_area_code});
      });

      causeDescRes.map((obj) => {
        this.wildfireTypeOpts.push({name: obj, code: obj});
      });

      this.dataReady = true;
    });
  }

  calculatexthPercentile(data: number[], percentile: number): number {
    const sortedData = data.sort((a, b) => a - b);
    const percentileIndex = Math.floor(percentile * (sortedData.length - 1));
    return sortedData[percentileIndex];
  }

  getMaxY(datasets: any[]): number {
    const allData = datasets.flatMap((dataset) => dataset.data);
    const maxY = this.calculatexthPercentile(allData, 1);
    return maxY * 1.2;
  }

  initializeChartData() {
    this.avgFireSizeData = {labels: this.chartLabels$(), datasets: this.avgFireSizeDataset$()};
    this.totalFireSizeData = {labels: this.chartLabels$(), datasets: this.totalFireSizeDataset$()};
    this.totalFireNumData = {labels: this.chartLabels$(), datasets: this.totalFireNumDataset$()};
    const options = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      }
    };

    this.avgFireSizeOpts = {
      ...options, scales: {
        y: {
          type: 'logarithmic',
          min: 0,
          max: this.getMaxY(this.avgFireSizeDataset$()),
        }
      }
    }
    this.totalFireSizeOpts = {
      ...options, scales: {
        y: {
          type: 'logarithmic',
          min: 0,
          max: this.getMaxY(this.totalFireSizeDataset$()),
        }
      }
    }
  }

  submitTypesForm() {
    this.dataReady = false;
    const formData: WildfireTypesBasedOnGeoFilters = {
      start_date: this.startDate$(),
      end_date: this.endDate$(),
      // geographic_area: !!this.geographicArea$() && this.geographicArea$().length !== 0 ? this.geographicArea$().map((val: any) => val.code) : undefined,
      cause_description: !!this.causeDescription$() && this.causeDescription$().length !== 0 ? this.causeDescription$().map((val: any) => val.code) : undefined
    };

    this.trendQueryService.getWildFireTypesBasedOnGeo(formData)
      .pipe((take(1)))
      .subscribe((res) => {
        // set labels
        const yearOfFireArray = res.map((resObj) => {
          return resObj.year_of_fire.toString();
        });
        const uniqueYearOfFireArray = Array.from(new Set(yearOfFireArray));
        this.chartLabels$.set(uniqueYearOfFireArray);


        const groupedData = new Map<string, WildfireTypesBasedOnGeoData[]>();

        res.forEach((obj) => {
          const key = `${obj.cause_description ?? 'Unknown'}`;
          if (!groupedData.has(key)) {
            groupedData.set(key, []);
          }
          groupedData.get(key)?.push(obj);
        });

        const avgFireSizeDatasets: any[] = [];
        const totalFireSizeDatasets: any[] = [];
        const totalFireNumDatasets: any[] = [];

        // Create datasets for each unique combination
        for (const [key, fires] of groupedData.entries()) {
          const label = key;

          avgFireSizeDatasets.push({
            label,
            data: fires.map((fire) => (fire.avg_fire_size)),
            fill: false,
            tension: 0.4
          });

          totalFireSizeDatasets.push({
            label,
            data: fires.map((fire) => (fire.total_fires_size)),
            fill: false,
            tension: 0.4
          });

          totalFireNumDatasets.push({
            label,
            data: fires.map((fire) => (fire.total_number_of_fires)),
            fill: false,
            tension: 0.4
          });
        }

        this.avgFireSizeDataset$.set(avgFireSizeDatasets);
        this.totalFireSizeDataset$.set(totalFireSizeDatasets);
        this.totalFireNumDataset$.set(totalFireNumDatasets);

        this.initializeChartData();
        this.dataReady = true;
      });
  }
}
