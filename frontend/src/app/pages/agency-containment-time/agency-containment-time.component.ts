import {Component, OnInit, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CalendarModule} from 'primeng/calendar';
import {ChartModule} from 'primeng/chart';
import {take} from 'rxjs/operators';
import {InputTextModule} from "primeng/inputtext";
import {TrendQueryService} from "../../core/services/trend_query_service";
import {AgencyContainmentTimeFilters} from "../../core/models/trend_query_dto.interface";
import {MultiSelectModule} from "primeng/multiselect";

interface ScatterDataset {
  x: number;
  y: number;
}

interface GroupedData {
  [unitName: string]: ScatterDataset[];
}

@Component({
  selector: "app-agency-containment-time",
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule, InputTextModule, MultiSelectModule],
  templateUrl: "./agency-containment-time.component.html",
  styleUrls: ["./agency-containment-time.component.css"],
})
export class AgencyContainmentTimeComponent implements OnInit {
  startDate$: WritableSignal<number | undefined> = signal(undefined);
  endDate$: WritableSignal<number | undefined> = signal(undefined);
  chartLabels$: WritableSignal<string[]> = signal([]);
  scatterDataOne$: WritableSignal<any> = signal({});
  barChartData$: WritableSignal<any> = signal({});
  scatterDataTwo$: WritableSignal<any> = signal({});

  options: any;
  scatterOpts: any;

  reportingAgencyOpts: any = [];
  reportingAgencies$: WritableSignal<any | undefined> = signal(undefined);

  dataReady = false;

  constructor(private trendQueryService: TrendQueryService) {
  }

  ngOnInit() {
    this.trendQueryService.getAgencyInformation()
      .pipe(take(1))
      .subscribe((res) => {
        res.map((obj) => this.reportingAgencyOpts.push({name: obj.agency_name, code: obj.agency_code}));
        this.initializeChartData();
        this.dataReady = true;
      })
  }

  initializeChartData() {
    this.options = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
    };

    this.scatterOpts = {
      scales: {
        y: {
          min: 0,
          max: 20000,
        },
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
    };
    this.scatterDataOne$.set({labels: [], datasets: []});
    this.barChartData$.set({labels: [], datasets: []});
    this.scatterDataTwo$.set({labels: [], datasets: []});
  }

  submitContainmentForm() {
    this.dataReady = false;
    const formData: AgencyContainmentTimeFilters = {
      start_date: this.startDate$(),
      end_date: this.endDate$(),
      reporting_agencies: !!this.reportingAgencies$() && this.reportingAgencies$().length !== 0 ? this.reportingAgencies$().map((val: any) => val.code) : undefined,
    };

    this.trendQueryService
      .getAgencyContainmentTime(formData)
      .pipe(take(1))
      .subscribe((res) => {
        const uniqueYears = Array.from(new Set(res.map((obj) => obj.year_of_fire.toString())));
        this.chartLabels$.set(uniqueYears);

        const groupedDataOne: GroupedData = {};
        const groupedDataTwo: GroupedData = {};
        // Scatter Plot - Relationship between Containment Time and Average Fire Size
        res.forEach((item) => {
          const unitName = item.reporting_unit_name || 'Unknown';
          if (!groupedDataOne[unitName]) {
            groupedDataOne[unitName] = [];
          }
          if (!groupedDataTwo[unitName]) {
            groupedDataTwo[unitName] = [];
          }

          groupedDataOne[unitName].push({
            x: item.time_to_contain,
            y: item.avg_size_of_fires,
          });
        });


        const scatterDataOne = Object.values(groupedDataOne).flat();
        const regressionLineOne = this.getRegressionLine(scatterDataOne);

        const scatterDataTwo = Object.values(groupedDataTwo).flat();
        const regressionLineTwo = this.getRegressionLine(scatterDataTwo);

        this.scatterDataOne$.set({
          labels: this.chartLabels$(), // Keep your existing labels
          datasets: [
            ...Object.entries(groupedDataOne).map(([key, values]) => ({
              label: key,
              data: values,
              backgroundColor: 'rgba(75, 192, 192, 0.5)',
              borderColor: 'rgba(75, 192, 192, 1)',
            })),
            {
              label: 'Regression Line',
              data: regressionLineOne,
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
              borderColor: 'rgba(255, 99, 132, 1)',
              type: 'line',
              pointRadius: 0,
              fill: false,
            },
          ],
        });

        const maxY = Math.max(...regressionLineOne.map((point) => point.y));
        this.scatterOpts = {
          ...this.scatterOpts, scales: {
            ...this.scatterOpts.scales, y: {
              min: 0,
              max: maxY * 1.2
            }
          }
        }
        // // Scatter Plot - Trends in Containment Time Over the Years
        // this.scatterDataTwo$.set({
        //   labels: this.chartLabels$(), // Keep your existing labels
        //   datasets: [
        //     ...Object.entries(groupedDataTwo).map(([key, values]) => ({
        //       label: key,
        //       data: values,
        //       backgroundColor: 'rgba(75, 192, 192, 0.5)',
        //       borderColor: 'rgba(75, 192, 192, 1)',
        //     })),
        //     {
        //       label: 'Regression Line',
        //       data: regressionLineOne,
        //       backgroundColor: 'rgba(255, 99, 132, 0.5)',
        //       borderColor: 'rgba(255, 99, 132, 1)',
        //       type: 'line',
        //       pointRadius: 0,
        //       fill: false,
        //     },
        //   ],
        // });
        //
        // // Bar Chart - Number of Fires by Reporting Agency
        // const agencies = Array.from(new Set(res.map((obj) => obj.reporting_unit_name)));
        //
        // this.barChartData$.set({
        //   labels: agencies,
        //   datasets: [
        //     {
        //       label: 'Total Fires by Agency',
        //       data: agencies.map((agency) =>
        //         res.filter((obj) => obj.reporting_unit_name === agency).reduce((total, curr) => total + curr.total_fires, 0),
        //       ),
        //       backgroundColor: 'rgba(255, 99, 132, 0.5)',
        //       borderColor: 'rgba(255, 99, 132, 1)',
        //     },
        //   ],
        // });

        this.dataReady = true;
      });
  }

  getRegressionLine(points: { x: number; y: number }[]) {
    const n = points.length;

    const sumX = points.reduce((sum, p) => sum + p.x, 0);
    const sumY = points.reduce((sum, p) => sum + p.y, 0);

    const sumXY = points.reduce((sum, p) => sum + p.x * p.y, 0);
    const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const xMin = Math.min(...points.map(p => p.x));
    const xMax = Math.max(...points.map(p => p.x));

    return [
      {x: xMin, y: slope * xMin + intercept},
      {x: xMax, y: slope * xMax + intercept},
    ];
  }
}
