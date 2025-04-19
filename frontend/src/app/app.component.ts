import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './layout/navbar/navbar.component';
// import { RouterOutlet } from '@angular/router';
import { MainPageComponent } from './pages/main-page/main-page.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  template: `
    <app-navbar></app-navbar>
    <router-outlet></router-outlet>
  `
})
export class AppComponent {
  title = 'frontend';
}
