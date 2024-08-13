import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { bangumiCard } from '../bangumi-card/bangumi-card';
import { cardData } from '../card';
import { CardService } from '../card-service';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog } from '@angular/material/dialog';
import { SubscriptionDialogComponent } from '../subscription-dialog/subscription-dialog.component';
import { NgSimpleSidebarModule, NgSimpleSidebarService, SimpleSidebarPosition, SimpleSidebarItem } from 'ng-simple-sidebar';



@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    bangumiCard,
    SidebarComponent,
    NgSimpleSidebarModule
  ],
  template: `
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
  <div class="content-wrapper">
	<lib-ng-simple-sidebar></lib-ng-simple-sidebar>
    <div class="content">
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
    </div>
  </div>
  `,
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {

  sidebarItems: SimpleSidebarItem[] = [];

  cardList: cardData[] = [];
  filteredCartList: cardData[] = [];
  CardsList: CardService = inject(CardService);
  dialog: MatDialog = inject(MatDialog);


  ngOnInit() {
    this.sidebarItems = [
      {
        name: '首页',
        icon: 'fas fa-home',
        routerLink: ['/'],
        position: SimpleSidebarPosition.top
      },
      {
        name: '系统日志',
        icon: 'fas fa-cog',
        routerLink: ['/systemInfo'],
        position: SimpleSidebarPosition.bottom
      }
    ];

    // Configure sidebar items and icons
    this.ngSimpleSidebarService.addItems(this.sidebarItems);
    this.ngSimpleSidebarService.configure({
      openIcon: 'fas fa-bars',
      closeIcon: 'fas fa-times'
    });

    // Optionally, manage the sidebar state
    this.ngSimpleSidebarService.open();
    this.ngSimpleSidebarService.close();


  }

  constructor(private ngSimpleSidebarService: NgSimpleSidebarService) {
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
    const dialogRef = this.dialog.open(SubscriptionDialogComponent, {
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
    const dialogRef = this.dialog.open(SubscriptionDialogComponent, {
      data: {
        title: '收集订阅',
        type: '2'
      }
    });
  }
}