import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink} from '@angular/router';
import {CardModule} from "primeng/card";

/**
 * The landing page component, it is an 'advertising' page of sorts.
 */
@Component({
  selector: 'landing-page',
  standalone: true,
  imports: [CommonModule, ButtonModule, RouterLink, CardModule],
  templateUrl: './landing.page.component.html',
  styleUrl: './landing.page.component.css'
})
export class LandingPageComponent {
  title = 'cis4301-project';

  /**
   * Scrolls the screen smoothly to the specified component/element.
   *
   * @param componentId the component/element id to scroll to
   */
  scrollToComponent(componentId: string): void {
    const element = document.getElementById(componentId);
    if (element) {
      element.scrollIntoView({behavior: 'smooth', block: 'start'});
    }
  }

}
