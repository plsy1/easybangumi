import { Component, Input, OnInit, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';
import { cardData, BangumiInfo } from '../card';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { BangumiInfoDialogComponent } from '../bangumi-info-dialog/bangumi-info-dialog.component'; // 确保路径正确

@Component({
  selector: 'app-bangumi-card',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  template: `
    <section class="listing-container">
      <section class="listing" >
        <img class="listing-photo" (click)="openBangumiInfoDialog()" [src]="imageUrl" alt="Exterior photo of {{cardInfo.title}}">
        <h3 class="listing-heading" (click)="openOnBangumi()" >{{ cardInfo.title }}</h3>
        <p class="listing-location">{{ cardInfo.season }}</p>
      </section>
    </section>
  `,
  styleUrls: ['./bangumi-card.css']
})
export class bangumiCard implements OnInit {
  @Input() cardInfo!: cardData;
  @Input() BangumiInfo!: BangumiInfo;
  @Output() subscriptionDeleted = new EventEmitter<string>();
  imageUrl: string | null = null;

  private apiUrlGetCover = 'http://localhost:18964/api/v1/info/getBangumiCover';
  private apiUrlGetBangumiInfo = 'http://localhost:18964/api/v1/info/getBangumiInfo';

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {
    if (this.cardInfo && this.cardInfo.bangumi_title) {
      this.loadImage(this.cardInfo.bangumi_title);
    }
  }

  loadImage(bangumi_title: string): void {
    const url = `${this.apiUrlGetCover}?name=${encodeURIComponent(bangumi_title)}`;

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
        title: this.cardInfo.bangumi_title,
        season: this.cardInfo.season,
        img: this.imageUrl,
        id: this.cardInfo.id
      }
    });

    dialogRef.componentInstance.subscriptionDeleted.subscribe(() => {
      this.handleSubscriptionDeleted();
    });
  }

  handleSubscriptionDeleted(): void {
    this.subscriptionDeleted.emit();
  }

  openOnBangumi(): void {
    if (this.cardInfo && this.cardInfo.bangumi_title) {
      this.loadBangumiInfo(this.cardInfo.bangumi_title).then(() => {
        if (this.BangumiInfo && this.BangumiInfo.id) {
          const baseUrl = 'https://bgm.tv/subject/';
          const url = `${baseUrl}${this.BangumiInfo.id}`;
          window.open(url, '_blank'); // 在新标签页中打开 URL
        } else {
          console.error('BangumiInfo or ID is not available');
        }
      }).catch(error => {
        console.error('Error loading Bangumi info:', error);
      });
    } else {
      console.error('cardInfo or bangumi_title is not available');
    }
  }

  async loadBangumiInfo(bangumi_title: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrlGetBangumiInfo}?bangumi_title=${encodeURIComponent(bangumi_title)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data: BangumiInfo = await response.json();
      this.BangumiInfo = data; // 将获取的数据赋值给 BangumiInfo
      console.log('Loaded Bangumi Info:', this.BangumiInfo);
    } catch (error) {
      console.error('Error loading Bangumi info:', error);
      // 处理错误
    }
  }
}