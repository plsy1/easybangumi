import { Component, Output, EventEmitter, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-subscription-dialog',
  templateUrl: './subscription-dialog.component.html',
  styleUrls: ['./subscription-dialog.component.css'],
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatSelectModule,
    CommonModule
    
  ]
})
export class SubscriptionDialogComponent {
  subscriptionType: string = '1';
  subscriptionText: string = '';
  private apiUrlAdd = 'http://localhost:12450/api/v1/rss/add';
  private apiUrlCollect = 'http://localhost:12450/api/v1/rss/collect';

  @Output() subscriptionAdded = new EventEmitter<void>();

  constructor(
    private dialogRef: MatDialogRef<SubscriptionDialogComponent>, 
    private snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data: { title: string; type: string }
  ) 
    {
      
    }
  

  submit_add() {
    const payload = {
      type: Number(this.subscriptionType),
      url: this.subscriptionText
    };
    
    fetch(this.apiUrlAdd, {
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
      console.log('添加订阅成功:', data);
      this.subscriptionAdded.emit();
      this.dialogRef.close();
    })
    .catch(error => {
      console.error('添加订阅失败:', error);
      this.showErrorNotification('添加订阅失败，请稍后再试。');
    });
  }

  submit_collect() {
    const payload = {
      url: this.subscriptionText
    };
    
    fetch(this.apiUrlCollect, {
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
      console.log('收集订阅成功:', data);
      this.subscriptionAdded.emit();
      this.dialogRef.close();
    })
    .catch(error => {
      console.error('收集订阅失败:', error);
      this.showErrorNotification('收集订阅失败，请稍后再试。');
    });
  }

  close() {
    this.dialogRef.close();
  }

  showErrorNotification(message: string) {
    this.snackBar.open(message, '关闭', {
      duration: 3000,
      panelClass: ['error-snackbar'] // Add custom styling if needed
    });
  }

}

