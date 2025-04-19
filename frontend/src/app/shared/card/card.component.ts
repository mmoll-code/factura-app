import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-card',
  imports: [CommonModule, RouterModule],
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss'],
  standalone: true
})
export class CardComponent {
  @Input() title = 'Card Test';
  @Input() header = 'My Header';
  @Input() description = 'My Description';
  @Input() image = ''; // '../../../assets/images/pexels-photo-bkg.jpeg' Ruta imagen de fondo
  @Input() link = '';  // routerLink destino
}