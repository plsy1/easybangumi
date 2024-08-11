import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BangumiInfoDialogComponent } from './bangumi-info-dialog.component';

describe('BangumiInfoDialogComponent', () => {
  let component: BangumiInfoDialogComponent;
  let fixture: ComponentFixture<BangumiInfoDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BangumiInfoDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BangumiInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
