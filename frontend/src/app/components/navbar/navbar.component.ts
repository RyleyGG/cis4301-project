import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ButtonModule} from 'primeng/button';
import {RouterLink, RouterLinkActive, RouterOutlet} from '@angular/router';
import {ThemeService} from '../../core/services/theme/theme.service';
import {ToggleButtonModule} from 'primeng/togglebutton';
import {ToolbarModule} from 'primeng/toolbar';
import {MenubarModule} from 'primeng/menubar';
import {firstValueFrom} from 'rxjs';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [ButtonModule, RouterLink, ToolbarModule, MenubarModule, RouterOutlet, ToolbarModule, RouterLinkActive, ToggleButtonModule, CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: 'navbar.component.css'
})
export class NavbarComponent implements OnInit {
  title = 'cis4301-project';
  loggedIn: boolean = false;

  async ngOnInit() {
  }

  constructor(private themeService: ThemeService) {
  }

  swapTheme(): void {
    const newTheme = this.themeService.theme() == 'arya-blue' ? 'saga-blue' : 'arya-blue';
    this.themeService.setTheme(newTheme);
  }
}
