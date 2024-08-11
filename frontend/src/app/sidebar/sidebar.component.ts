import { Component } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  template: `
    <nav class="sidebar">
      <ul>
        <li><a routerLink="/home">番剧订阅</a></li>
        <li><a routerLink="/contact">系统日志</a></li>
        <li><a routerLink="/contact">全局设置</a></li>
      </ul>
    </nav>
  `,
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  // 你可以在这里添加任何需要的逻辑
}