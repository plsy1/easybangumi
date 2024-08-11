import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HousingLocationComponent } from '../bangumi-card/bangumi-card';
import { HousingLocation } from '../card';
import { HousingService } from '../card-service';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MatDialog } from '@angular/material/dialog';
import { SubscriptionDialogComponent } from '../subscription-dialog/subscription-dialog.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HousingLocationComponent,
    SidebarComponent,
  ],
  template: `
  <app-sidebar></app-sidebar>
  <section class="search-bar">
    <form>
      <input type="text" placeholder="以番剧名称搜索" #filter>
      <button class="primary" type="button" (click)="filterResults(filter.value)">搜索订阅</button>
      <button class="primary" type="button" (click)="addSubscription()">添加订阅</button>
      <button class="primary" type="button" (click)="addSubscription()">收集订阅</button>
    </form>
  </section>
  <section class="results">
    <app-bangumi-card 
      *ngFor="let housingLocation of filteredLocationList" 
      [housingLocation]="housingLocation"
      (subscriptionDeleted)="handleSubscriptionDeleted()">
    </app-bangumi-card>
  </section>
  `,
  styleUrls: ['./home.component.css'],
})
export class HomeComponent {

  housingLocationList: HousingLocation[] = [];
  filteredLocationList: HousingLocation[] = [];
  housingService: HousingService = inject(HousingService);
  dialog: MatDialog = inject(MatDialog);

  constructor() {
    this.loadHousingLocations();
  }

  loadHousingLocations() {
    this.housingService.getAllHousingLocations().then((housingLocationList: HousingLocation[]) => {
      this.housingLocationList = housingLocationList;
      this.filteredLocationList = housingLocationList;
    });
  }

  filterResults(text: string) {
    if (!text) {
      this.filteredLocationList = this.housingLocationList;
      return;
    }

    this.filteredLocationList = this.housingLocationList.filter(
      housingLocation => housingLocation?.title.toLowerCase().includes(text.toLowerCase())
    );
  }

  addSubscription() {
    const dialogRef = this.dialog.open(SubscriptionDialogComponent);

    dialogRef.componentInstance.subscriptionAdded.subscribe(() => {
      this.loadHousingLocations(); // 订阅成功后重新加载数据
    });
  }

  handleSubscriptionDeleted() {
    this.loadHousingLocations(); // 订阅成功后重新加载数据
  }
}