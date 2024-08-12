import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterModule,
  ],
  template: `
    <section>
      <router-outlet></router-outlet>
    </section>
  `,
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
}


