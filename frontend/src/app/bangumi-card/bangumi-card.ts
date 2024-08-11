import { Component, Input, OnInit, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HousingLocation } from '../card';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { BangumiInfoDialogComponent } from '../bangumi-info-dialog/bangumi-info-dialog.component'; // 确保路径正确

@Component({
  selector: 'app-bangumi-card',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  template: `
    <section class="listing-container">
      <section class="listing" (click)="openBangumiInfoDialog()">
        <img class="listing-photo" [src]="imageUrl" alt="Exterior photo of {{housingLocation.title}}">
        <h3 class="listing-heading">{{ housingLocation.title }}</h3>
        <p class="listing-location">{{ housingLocation.season }}</p>
      </section>
    </section>
  `,
  styleUrls: ['./bangumi-card.css']
})
export class HousingLocationComponent implements OnInit {
  @Input() housingLocation!: HousingLocation;
  @Output() subscriptionDeleted = new EventEmitter<string>();
  imageUrl: string | null = null;

  private apiUrl = 'http://localhost:18964/api/v1/info/getBangumiCover';

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {
    if (this.housingLocation && this.housingLocation.bangumi_title) {
      this.loadImage(this.housingLocation.bangumi_title);
    }
  }

  loadImage(bangumi_title: string): void {
    const url = `${this.apiUrl}?name=${encodeURIComponent(bangumi_title)}`;

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch image');
        }
        return response.blob();
      })
      .then(blob => {
        this.imageUrl = URL.createObjectURL(blob);
      })
      .catch(error => {
        console.error('Failed to load image', error);
      });
  }

  openBangumiInfoDialog() {
    const dialogRef = this.dialog.open(BangumiInfoDialogComponent, {
      data: {
        title: this.housingLocation.bangumi_title,
        season: this.housingLocation.season,
        img: this.imageUrl,
        id: this.housingLocation.id
      }
    });

    dialogRef.componentInstance.subscriptionDeleted.subscribe(() => {
      this.handleSubscriptionDeleted();
    });
  }

  handleSubscriptionDeleted(): void {
    this.subscriptionDeleted.emit();
  }
}