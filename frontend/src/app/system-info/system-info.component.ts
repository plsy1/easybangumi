import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { LogsData } from '../logs';

@Component({
  selector: 'app-system-info',
  standalone: true,
  imports: [SidebarComponent, CommonModule],
  templateUrl: './system-info.component.html',
  styleUrls: ['./system-info.component.css']
})
export class SystemInfoComponent implements OnInit, OnDestroy {
  logData?: LogsData;  // 用于存储日志数据
  loading = true;   // 加载状态
  private apiUrl = 'http://localhost:18964/api/v1/info/getSystemLogs'; 
  private intervalId?: number; // 定时器ID

  constructor() {}

  ngOnInit() {
    this.loadLogs();
    this.intervalId = window.setInterval(() => this.loadLogs(), 10000); 
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