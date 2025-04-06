import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MainPageComponent } from './pages/main-page/main-page.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MainPageComponent],
  template: `<app-main-page />`
})
export class AppComponent {
  title = 'frontend';
}
