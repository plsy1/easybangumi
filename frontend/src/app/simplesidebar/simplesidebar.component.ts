import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgSimpleSidebarModule, NgSimpleSidebarService, SimpleSidebarPosition, SimpleSidebarItem } from 'ng-simple-sidebar';

@Component({
  selector: 'app-simplesidebar',
  standalone: true,
  templateUrl: './simplesidebar.component.html',
  styleUrl: './simplesidebar.component.css',
  imports: [CommonModule, NgSimpleSidebarModule] // Import the library module here
})
export class SimplesidebarComponent implements OnInit {
  sidebarItems: SimpleSidebarItem[] = [];

  constructor(private ngSimpleSidebarService: NgSimpleSidebarService) {}

  ngOnInit() {
    this.sidebarItems = [
      {
        name: '订阅',
        icon: 'fas fa-home',
        routerLink: ['/'],
        position: SimpleSidebarPosition.top
      },
      {
        name: 'secanis.ch',
        icon: 'fas fa-home',
        url: 'systemInfo',
        target: '_blank',
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
}

