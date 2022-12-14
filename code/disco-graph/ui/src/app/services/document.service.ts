import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Publication } from '../model/publication';
import { KeywordService } from './keyword.service';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  constructor(
    private keywordService: KeywordService,
  ) { }

  getDocument(id: string): Observable<Publication> {
    let cachedDoc = this.keywordService.searchResults.find((document) => document.publication_id === id);
    if (cachedDoc){
      return of(cachedDoc);
    }
    return of({
    publication_id: 'test_id',
    author: 'daniel gomm',
    title: 'disco graph - graph based knwoledge discovery gone disco!',
    doi: '0932u487934857',
    issued: 2023,
    created: 2022,
    language: 'en',
    keywords: [{
      values: [{
        value: 'discovery',
        language: 'en'
      },
      {
        value: 'entdeckung',
        language: 'de'
      }],
      verification_status: 3
    }],
    additional_attributes: [{
      name: 'university',
      value: 'kit',
      verification_status: 1
    },
    {
      name: 'version management',
      value: 'git',
      verification_status: 7
    }]
    })
  }


}
