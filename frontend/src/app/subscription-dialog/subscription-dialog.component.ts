import { Component, Output, EventEmitter } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-subscription-dialog',
  templateUrl: './subscription-dialog.component.html',
  styleUrls: ['./subscription-dialog.component.css'],
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ]
})
export class SubscriptionDialogComponent {
  subscriptionText: string = '';
  private apiUrl = 'http://localhost:18964/api/v1/rss/add';

  @Output() subscriptionAdded = new EventEmitter<void>();

  constructor(private dialogRef: MatDialogRef<SubscriptionDialogComponent>) {}

  submit() {
    const payload = {
      type: 1,
      url: this.subscriptionText
    };
    
    fetch(this.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('订阅成功:', data);
      this.subscriptionAdded.emit(); // 通知父组件订阅已添加
      this.dialogRef.close();
    })
    .catch(error => {
      console.error('订阅失败:', error);
    });
  }

  close() {
    this.dialogRef.close();
  }
}