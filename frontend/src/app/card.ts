export interface HousingLocation {
    id: number;
    link: string;
    title: string;
    season: string;
    bangumi_title: string;
  }

  export interface ApiResponse<T> {
    success: boolean;
    message?: string;
    data?: T;
  }