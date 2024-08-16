import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { LogsData } from '../logs';
import { NgSimpleSidebarModule, NgSimpleSidebarService, SimpleSidebarPosition, SimpleSidebarItem } from 'ng-simple-sidebar';

@Component({
  selector: 'app-system-info',
  standalone: true,
  imports: [SidebarComponent, CommonModule, NgSimpleSidebarModule],
  templateUrl: './system-info.component.html',
  styleUrls: ['./system-info.component.css']
})
export class SystemInfoComponent implements OnInit, OnDestroy {
  logData?: LogsData;  // 用于存储日志数据
  loading = true;   // 加载状态
  private apiUrl = 'http://localhost:12450/api/v1/info/getSystemLogs'; 
  private intervalId?: number; // 定时器ID
  sidebarItems: SimpleSidebarItem[] = [];

  constructor(private ngSimpleSidebarService: NgSimpleSidebarService) {

  }


  ngOnInit() {
    this.loadLogs();
    this.intervalId = window.setInterval(() => this.loadLogs(), 10000); 
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
      openIcon: 'las la-bars',
      closeIcon: 'las la-times'
    });

    // Optionally, manage the sidebar state
    this.ngSimpleSidebarService.open();
    this.ngSimpleSidebarService.close();

    
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId); // 清除定时器，避免内存泄漏
    }
  }

  async loadLogs() {
    try {
      const response = await fetch(this.apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data: LogsData = await response.json();
      this.logData = data;
      console.log(data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      this.loading = false;
    }
  }
}