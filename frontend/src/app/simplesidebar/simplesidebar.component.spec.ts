import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimplesidebarComponent } from './simplesidebar.component';

describe('SimplesidebarComponent', () => {
  let component: SimplesidebarComponent;
  let fixture: ComponentFixture<SimplesidebarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SimplesidebarComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SimplesidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
