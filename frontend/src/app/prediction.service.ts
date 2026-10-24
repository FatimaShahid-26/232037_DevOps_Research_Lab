import {Injectable, inject} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { timeout } from 'rxjs';
export interface PredictionResponse {
 prediction:number; label:string; probabilities: Record<string, number>;
 model_version:string; disclaimer:string;
}
@Injectable({providedIn:'root'})
export class PredictionService {
 private http=inject(HttpClient);
 predict(payload:Record<string,number>){return this.http
  .post<PredictionResponse>('/api/predict', payload)
  .pipe(timeout(30000));}
}
