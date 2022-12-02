import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { ValueWithLanguage } from "src/app/model/publication";

@Injectable()
export class KeywordCompletionService {

    private BASE_URL = 'http://localhost:5000/api/v1/';
    
    constructor(private http: HttpClient){

    }

    getKeywords(inputValue: string | null): Observable<ValueWithLanguage[]> {
        if (inputValue == null) {
          inputValue = ''
        };
        return this.http.get<ValueWithLanguage[]>(`${this.BASE_URL}keyword/load?keys=${inputValue}`)
      }

}