import { HttpBackend, HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Keyword, Publication } from '../model/publication';
import { DocumentTitleResponse } from '../model/responses';
import { KeywordService } from './keyword.service';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  constructor(
    private keywordService: KeywordService,
    private http: HttpClient
  ) { }

  getDocument(id: string): Observable<Publication> {
    return this.http.get<Publication>(`/api/publication/${id}`);
  }

  getDocumentTitles(searchInput: string, limit: number, page: number): Observable<DocumentTitleResponse[]>{
    return this.http
    .get<DocumentTitleResponse[]>(`/api/publication/list?limit=${limit}&keys=${searchInput}&page=${page}`);
  }

  addKeyword(publication: Publication, keyword: Keyword): Observable<string>{
    return this.http.post<string>(`/api/publication/${publication.publication_id}/keyword`, keyword);
  }

}
