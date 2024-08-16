import { Component, Inject, Output, EventEmitter } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-bangumi-info-dialog',
  standalone: true,
  imports: [
    MatDialogModule,
  ],
  templateUrl: './bangumi-info-dialog.component.html',
  styleUrls: ['./bangumi-info-dialog.component.css']
})
export class BangumiInfoDialogComponent {
  constructor(
    private dialogRef: MatDialogRef<BangumiInfoDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { title: string; season: string; img: string; id: string }
  ) {}

  private apiUrl = 'http://localhost:12450/api/v1/rss/delete';

  @Output() subscriptionDeleted = new EventEmitter<void>();

  deleteSubscription(id: string, type: number = 1) {
    const body = {
      type: type,
      id: id
    };

    fetch(this.apiUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      console.log('订阅删除成功');
      this.subscriptionDeleted.emit(); // 通知父组件订阅已添加
      this.close();
    })
    .catch(error => {
      console.error('删除订阅时发生错误:', error);
    });
  }

  close() {
    this.dialogRef.close();
  }
}