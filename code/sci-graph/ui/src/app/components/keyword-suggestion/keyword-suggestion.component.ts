import { Component, OnInit } from '@angular/core';
import { ValueWithLanguage } from 'src/app/model/publication';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-keyword-suggestion',
  templateUrl: './keyword-suggestion.component.html',
  styleUrls: ['./keyword-suggestion.component.scss']
})
export class KeywordSuggestionComponent implements OnInit {

  constructor(
    private keywordService: KeywordService,
  ){
  }

ngOnInit(): void {
    
}

getKeywordSuggestions(): ValueWithLanguage[]{
  return this.keywordService.keywordSuggestions;
}

removeSuggestion(keywordSuggestion: ValueWithLanguage): void{
  const index = this.keywordService.keywordSuggestions.indexOf(keywordSuggestion);

  if (index >= 0){
    this.keywordService.keywordSuggestions.splice(index, 1);
  }
  this.keywordService.addKeywordSelection(keywordSuggestion);
  //this.keywordService.selectedKeywords.push(keywordSuggestion);
}

isLoading(){
  return this.keywordService.loadingKeywordSuggestions;
}

}
