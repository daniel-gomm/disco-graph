import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

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
    })
  }

  deleteYearsFilter(): Observable<any>{
    return this.http.delete('/api/v1/filter/year');
  }

}
