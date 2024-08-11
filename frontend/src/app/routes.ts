import { SidebarComponent } from './sidebar/sidebar.component';
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

const routeConfig: Routes = [
    {
      path: '',
      component: HomeComponent,
      title: 'EasyBangumi - 全自动追番'
    }
  ];
  
  export default routeConfig;