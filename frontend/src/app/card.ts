export interface cardData {
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

export interface BangumiInfo {
  id: string; 
  eps: { [key: string]: number };
  total: number;
}