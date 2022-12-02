import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { ValueWithLanguage } from "src/app/model/publication";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KeywordService {

  constructor(
    private http: HttpClient
  ) { }

  getKeywords(inputValue:string | null, limit: number = 10): Observable<ValueWithLanguage[]>{
    if (inputValue === ""){
      inputValue = "*";
    }
    return this.http.get<ValueWithLanguage[]>(`/api/v1/keyword/load?keys=${inputValue}&limit=${limit}`);
  }

}
