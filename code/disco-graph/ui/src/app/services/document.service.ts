import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Publication } from '../model/publication';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  constructor() { }

  getDocument(id: string): Observable<Publication> {
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
