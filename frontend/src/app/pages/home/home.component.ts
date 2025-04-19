import { Component } from '@angular/core';
import { CardComponent } from "../../shared/card/card.component";

@Component({
  selector: 'app-home',
  imports: [CardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
