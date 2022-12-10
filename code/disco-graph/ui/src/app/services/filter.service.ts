import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AttributeResponse } from '../model/responses';

@Injectable({
  providedIn: 'root'
})
export class FilterService {

  filtersChanged: boolean = false;

  constructor(
    private http: HttpClient,
  ) { }

  setYearsFilter(startYear:number, endYear:number): Observable<any>{
    return this.http.post('/api/v1/filter/year', {
      lower_limit: startYear,
      upper_limit: endYear
    });
  }

  deleteYearsFilter(): Observable<any>{
    return this.http.delete('/api/v1/filter/year');
  }

  getAttributes(): Observable<AttributeResponse[]>{
    return this.http.get<AttributeResponse[]>('/api/v1/filter/attribute');
  }

  setAttributeFilter(attributeName: string, attributeValue:string): Observable<any> {
    return this.http.post('/api/v1/filter/attribute', {
      name: attributeName,
      value: attributeValue
    });
  }

  deleteAttributeFilter(attributeName: string): Observable<any>{
    return this.http.delete(`/api/v1/filter/attribute/${attributeName}`)
  }

}
