import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FilterService {

  filtersChanged: boolean = false;

  constructor(
    http: HttpClient,
  ) { }

}
