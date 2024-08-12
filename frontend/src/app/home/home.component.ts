import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { bangumiCard } from '../bangumi-card/bangumi-card';
import { cardData } from '../card';
import { CardService } from '../card-service';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog } from '@angular/material/dialog';
import { SubscriptionDialogComponent } from '../subscription-dialog/subscription-dialog.component';
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    bangumiCard,
    SidebarComponent,
    
  ],
  template: `
  <app-sidebar></app-sidebar>
  <section class="search-bar">
    <form>
      <input type="text" placeholder="以番剧名称搜索" #filter (input)="filterResults(filter.value)">
      <button class="primary" type="button" (click)="addSubscription()">添加订阅</button>
      <button class="primary" type="button" (click)="collectSubscription()">收集订阅</button>
    </form>
  </section>
  <section class="results">
    <app-bangumi-card 
      *ngFor="let cardInfo of filteredCartList" 
      [cardInfo]="cardInfo"
      (subscriptionDeleted)="handleSubscriptionDeleted()">
    </app-bangumi-card>
  </section>
  `,
  styleUrls: ['./home.component.css'],
})
export class HomeComponent {

  cardList: cardData[] = [];
  filteredCartList: cardData[] = [];
  CardsList: CardService = inject(CardService);
  dialog: MatDialog = inject(MatDialog);

  constructor() {
    this.loadCards();
  }

  loadCards() {
    this.CardsList.getAllCards().then((cardList: cardData[]) => {
      this.cardList = cardList;
      this.filteredCartList = cardList;
    });
  }

  filterResults(text: string) {
    if (!text) {
      this.filteredCartList = this.cardList;
      return;
    }

    this.filteredCartList = this.cardList.filter(
      cardInfo => cardInfo?.title.toLowerCase().includes(text.toLowerCase())
    );
  }

  addSubscription() {
    const dialogRef = this.dialog.open(SubscriptionDialogComponent,{
      data: {
        title: '添加订阅',
        type: '1'
      }
    });

    dialogRef.componentInstance.subscriptionAdded.subscribe(() => {
      this.loadCards(); // 订阅成功后重新加载数据
    });
  }

  handleSubscriptionDeleted() {
    this.loadCards(); // 订阅成功后重新加载数据
  }

  collectSubscription() {
    const dialogRef = this.dialog.open(SubscriptionDialogComponent,{
      data: {
        title: '收集订阅',
        type: '2'
      }
    });
  }
}