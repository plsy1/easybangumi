import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SystemInfoComponent } from './system-info/system-info.component';
import { SimplesidebarComponent } from './simplesidebar/simplesidebar.component'
const routeConfig: Routes = [
    {
      path: '',
      component: HomeComponent,
      title: '番剧订阅 - EasyBangumi - 全自动追番'
    },
    {
      path: 'systemInfo',
      component: SystemInfoComponent,
      title: '系统日志 - EasyBangumi - 全自动追番'
    },
    {
      path: 'test',
      component: SimplesidebarComponent,
      title: '测试页面 - EasyBangumi - 全自动追番'
    },
  ];
  
  export default routeConfig;