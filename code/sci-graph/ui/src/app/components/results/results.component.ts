import { Component, OnInit } from '@angular/core';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit{

  constructor(
    private keywordService: KeywordService,
  ){}


ngOnInit(): void {
    
}

isLoading(): boolean{
  return this.keywordService.loadingSearchResults;
}

getResults(): Publication[]{
  return this.keywordService.searchResults;
}

extractKeyword(keyword: Keyword): ValueWithLanguage{
  let value = keyword.values.at(0);
  if(value){
    return value;
  }
  return {value: '', language:'none'}
}

}
