import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatusService {

  constructor(
    private http: HttpClient
  ) { }

  updateKeywordVerification(publicationIdentifier: string, keywordIdentifier: string, newVerificationStatus: number): Observable<any>{
    return this.http.put(`/publication/${publicationIdentifier}/keyword/${keywordIdentifier}/verification_status`, 
    {verification_status: newVerificationStatus},
    {responseType: 'text'});
  }

}
