import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Publication, ValueWithLanguage } from "src/app/model/publication";
import { finalize, Observable, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KeywordService {

  keywordSuggestions: ValueWithLanguage[] = [];
  selectedKeywords: ValueWithLanguage[] = [];

  filteredKeywords: ValueWithLanguage[] = [];
  autocompletesuggestionLimit: number = 10;
  cachedPreviousInput: string = "";

  searchResults: Publication[] = [];
  loadingSearchResults: boolean = false;

  loadingKeywordSuggestions: boolean = false;

  constructor(
    private http: HttpClient
  ) { }

  getAutocompleteSuggestion(input: string | null): Observable<ValueWithLanguage[]>{
    if(input === null || input === ""){
      //input = "*";
      this.cachedPreviousInput = "__no_input";
      return of([]);
    }
    if (input !== "*" && this.filteredKeywords.length < this.autocompletesuggestionLimit && input.startsWith(this.cachedPreviousInput)){
      this.cachedPreviousInput = input;
      return of(this._filterCachedSuggestions(input))
    }
    this.cachedPreviousInput = input;
    return this.getKeywords(input, this.autocompletesuggestionLimit);
  }

  private _filterCachedSuggestions(inputValue: string): ValueWithLanguage[] {
    const filterValue = inputValue.toLowerCase();

    return this.filteredKeywords.filter(keyword => keyword.value.toLowerCase().includes(filterValue));
  }


  getKeywords(inputValue:string | null, limit: number = 10): Observable<ValueWithLanguage[]>{
    if (inputValue === ""){
      inputValue = "*";
    }
    return this.http.get<ValueWithLanguage[]>(`/api/api/v1/keyword/load?keys=${inputValue}&limit=${limit}`);
  }

  addKeywordSelection(selectedKeyword: ValueWithLanguage):void {
    this.selectedKeywords.push(selectedKeyword);
    this.loadKeywordSuggestions();
    this.loadSearchResults();
  }

  removeKeywordSelection(keyword: ValueWithLanguage): void{
    const index = this.selectedKeywords.indexOf(keyword);
    if(index >= 0){
      this.selectedKeywords.splice(index, 1);
      this.loadKeywordSuggestions();
      this.loadSearchResults();
    }
  }

  private loadKeywordSuggestions():void {
    this.loadingKeywordSuggestions = true;
    this.getKeywordCrossRererence().pipe(
      finalize(() => {
        this.loadingKeywordSuggestions = false;
      })
    )
    .subscribe((res: ValueWithLanguage[]) => {
      this.keywordSuggestions = res;
    })
  }

  private loadSearchResults(): void {
    this.loadingSearchResults = true;
    this.getResults().pipe(
      finalize(() => {
        this.loadingSearchResults = false;
      })
    )
    .subscribe((res: Publication[]) => {
      this.searchResults = res;
    })
  }

  getKeywordCrossRererence(limit: number = 10):Observable<ValueWithLanguage[]>{
    if (this.selectedKeywords.length === 0){
      return of([]);
    }
    return this.http.get<ValueWithLanguage[]>
    (`/api/api/v1/keyword/cross-reference?keywords=${this.createKeywordQuery(this.selectedKeywords)}&limit=${limit}`);
  }

  getResults(limit: number = 10): Observable<Publication[]>{
    if (this.selectedKeywords.length === 0){
      return of([]);
    }
    return this.http.get<Publication[]>
    (`/api/api/v1/publication/results?keywords=${this.createKeywordQuery(this.selectedKeywords)}&limit=${limit}`)
  }

  createKeywordQuery(keywords: ValueWithLanguage[]): string{
    let result = "";
    keywords.forEach(keyword => {
      result += `${keyword.value}@${keyword.language},`;
    });
    return result.slice(0, -1);
  }

  getLanguages(): Observable<[string]> {
    return this.http.get<[string]>(`/api/keyword/languages`);
  }

}
