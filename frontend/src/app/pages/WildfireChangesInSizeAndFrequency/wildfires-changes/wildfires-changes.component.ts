import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CalendarModule } from 'primeng/calendar';
import { ChartModule } from 'primeng/chart';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-wildfires-changes',
  standalone: true,
  imports: [CalendarModule, FormsModule, ChartModule],
  templateUrl: './wildfires-changes.component.html',
  styleUrl: './wildfires-changes.component.css'
})

export class WildfiresChangesComponent {
  startDate: Date = new Date();  // Date property for calendar binding
  endDate: Date = new Date();  // Date property for calendar binding

  data: any;
  options: any;

  constructor(private http: HttpClient) {  // Inject HttpClient here
    this.initializeChartData();
  }

  initializeChartData() {
    this.data = {
      labels: ['2000', '2001', '2002', '2003', '2004', '2005', '2006'],
      datasets: [
        {
          label: 'Demo Data',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#42A5F5'
        }
      ]
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
    const formData = {
      startDate: this.startDate,
      endDate: this.endDate
    };
  
    this.http.post('http://127.0.0.1:8000/dummy/changes-in-size-and-frequency-form-submission', formData).subscribe({
      next: (response) => console.log('Form submitted successfully', response),
      error: (error) => console.error('Error submitting form', error)
    });
  }
}