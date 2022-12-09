import { Component, Input, OnInit } from '@angular/core';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-result-item',
  templateUrl: './result-item.component.html',
  styleUrls: ['./result-item.component.scss']
})
export class ResultItemComponent implements OnInit{

  @Input() publication: Publication | undefined = undefined;

  constructor (
    private keywordService: KeywordService,
  ) {}
  
  ngOnInit():void {

  }

  extractKeyword(keyword: Keyword): ValueWithLanguage{
    let value = keyword.values.at(0);
    if(value){
      return value;
    }
    return {value: '', language:'none'}
  }

  getKeywords(): ValueWithLanguage[] {
    let result: ValueWithLanguage[] = [];
    this.publication?.keywords?.forEach(kw => {
      let value = kw.values.at(0);
      if (value){
        result.push(value);
      }
    })
    return result;
  }

  isMatched(keyword:ValueWithLanguage): boolean{
    return Boolean(this.keywordService.selectedKeywords.find(kw => kw.value === keyword.value));
  }

  addKeyword(kw: ValueWithLanguage){
    this.keywordService.addKeywordSelection(kw);
  }

}
