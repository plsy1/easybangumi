import { Injectable } from '@angular/core';
import { ApiResponse, HousingLocation } from './card';

@Injectable({
  providedIn: 'root'
})
export class HousingService {

  constructor() { }

  url = 'http://localhost:18964/api/v1/info/getBangumiSubscription';

  async getAllHousingLocations(): Promise<HousingLocation[]> {
    try {
      const response = await fetch(this.url);
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data: ApiResponse<HousingLocation[]> = await response.json();

      if (data.success) {
        return data.data ?? [];
      } else {
        console.error('API 错误:', data.message);
        return [];
      }
    } catch (error) {
      console.error('请求失败:', error);
      return [];
    }
  }
  async getHousingLocationById(id: number): Promise<HousingLocation | undefined> {
    const data = await fetch(`${this.url}/${id}`);
    return await data.json() ?? {};
  }

  submitApplication(firstName: string, lastName: string, email: string) {
    console.log(`Homes application received: firstName: ${firstName}, lastName: ${lastName}, email: ${email}.`);
  }

}
