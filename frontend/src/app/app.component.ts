import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink, RouterLinkActive, RouterOutlet} from '@angular/router';
import {NavbarComponent} from './components/navbar/navbar.component';
import {ToggleButtonModule} from 'primeng/togglebutton';
import {MenubarModule} from 'primeng/menubar';
import {DialogModule} from 'primeng/dialog';
import {ConfirmationService, MessageService} from 'primeng/api';
import { HttpClientModule } from '@angular/common/http';


/**
 * The main application component, currently the sample hello world page.
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ToggleButtonModule, DialogModule, MenubarModule, RouterOutlet, NavbarComponent, ButtonModule, RouterLink, RouterLinkActive, HttpClientModule],
  providers: [ConfirmationService, MessageService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'cis4301-project';
}
