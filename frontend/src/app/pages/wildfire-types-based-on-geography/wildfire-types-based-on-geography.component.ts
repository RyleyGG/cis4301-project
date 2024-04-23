import {Component, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CalendarModule} from 'primeng/calendar';
import {ChartModule} from 'primeng/chart';
import {HttpClient} from '@angular/common/http';
import {
  wildfireSizeBasedOnGeoFilters, WildfireTypesBasedOnGeoData,
  WildfireTypesBasedOnGeoFilters
} from "../../core/models/trend_query_dto.interface";
import {TrendQueryService} from "../../core/services/trend_query_service";
import {take} from "rxjs";
import {InputTextModule} from "primeng/inputtext";
import {DropdownModule} from "primeng/dropdown";
import {MultiSelectModule} from "primeng/multiselect";  // Make sure to import HttpClient


@Component({
  selector: 'app-wildfire-types-based-on-geography',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule, InputTextModule, DropdownModule, MultiSelectModule],  // Include FormsModule here
  templateUrl: './wildfire-types-based-on-geography.component.html',
  styleUrls: ['./wildfire-types-based-on-geography.component.css']  // Corrected property name and syntax
})

export class wildfireTypesBasedOnGeographyComponent {
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

  options: any;
  dataReady = true

  geographicAreaOpts: any = [
    {name: "Canadian Interagency Forest Fire Centre", code: "CAMBCIFC"},
    {name: "Alaska Interagency Coordination Center", code: "USAKCC"},
    {name: "Northern California Area Coordination Center", code: "USCAONCC"},
    {name: "Southern California Coordination Center", code: "USCAOSCC"},
    {name: "Rocky Mountain Area Coordination Center", code: "USCORMCC"},
    {name: "Southern Area Coordination Center", code: "USGASAC"},
    {name: "National Interagency Coordination Center", code: "USIDNIC"},
    {name: "Northern Rockies Coordination Center", code: "USMTNRC"},
    {name: "Southwest Area Coordination Center", code: "USNMSWC"},
    {name: "Northwest Area Coordination Center", code: "USORNWC"},
    {name: "Western Great Basin Coordination Center", code: "USUTGBC"},
    {name: "Eastern Area Coordination Center", code: "USWIEACC"},
  ];

  wildfireTypeOpts: any = [
    {name: "Powerline", code: "Powerline"},
    {name: "Equipment Use", code: "Equipment Use"},
    {name: "Arson", code: "Arson"},
    {name: "Missing/Undefined", code: "Missing/Undefined"},
    {name: "Fireworks", code: "Fireworks"},
    {name: "Campfire", code: "Campfire"},
    {name: "Railroad", code: "Railroad"},
    {name: "Lightning", code: "Lightning"},
    {name: "Miscellaneous", code: "Miscellaneous"},
    {name: "Structure", code: "Structure"},
    {name: "Children", code: "Children"},
    {name: "Debris Burning", code: "Debris Burning"},
    {name: "Smoking", code: "Smoking"},
  ];

  constructor(private http: HttpClient, private trendQueryService: TrendQueryService) {
  }

  initializeChartData() {
    this.avgFireSizeData = {labels: this.chartLabels$(), datasets: this.avgFireSizeDataset$()};
    this.totalFireSizeData = {labels: this.chartLabels$(), datasets: this.totalFireSizeDataset$()};
    this.totalFireNumData = {labels: this.chartLabels$(), datasets: this.totalFireNumDataset$()};
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
    this.dataReady = false;
    const formData: WildfireTypesBasedOnGeoFilters = {
      start_date: this.startDate$(),
      end_date: this.endDate$(),
      geographic_area: !!this.geographicArea$() && this.geographicArea$().length !== 0 ? this.geographicArea$().map((val: any) => val.code) : undefined,
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
          const key = `${obj.cause_description ?? 'Unknown'} - ${obj.geographic_area_code ?? 'Unknown'}`;
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
