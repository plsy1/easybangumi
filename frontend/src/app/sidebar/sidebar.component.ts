import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterModule], // 引入 RouterModule
  template: `
    <nav class="sidebar">
    <ul class="highlight-ul1">
      <li>
        <a
          routerLink="/"
          routerLinkActive="active-link"
          [routerLinkActiveOptions]="{ exact: true }"
        >
        番剧订阅
        </a>
      </li>
    </ul>
    <ul class="highlight-ul2">
      <li>
        <a
          routerLink="/systemInfo"
          routerLinkActive="active-link"
        >
        系统日志
        </a>
      </li>
    </ul>
    </nav>
  `,
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  constructor(private router: Router) {}

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
}