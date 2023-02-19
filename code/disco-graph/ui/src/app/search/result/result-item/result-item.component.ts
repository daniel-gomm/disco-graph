import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
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
    private router: Router
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

  extractFittingKeywordValue(keyword:Keyword): ValueWithLanguage{
    // Try to extract the keyword value in the publication language,if not possible return any value
    let valueWithLanguage = keyword.values.find(valueWithLanguage => valueWithLanguage.language === this.publication?.language);
    if(valueWithLanguage){
      return valueWithLanguage;
    }
    let valueWithUnfittingLanguage = keyword.values.at(0);
    if(valueWithUnfittingLanguage){
      return valueWithUnfittingLanguage;
    }
    return {value: '', language: 'undefined'};
  }

  isMatched(keyword:Keyword): boolean{
    return Boolean(keyword.values.find(kwValue => Boolean(this.keywordService.selectedKeywords.find(val => val.value == kwValue.value))));
  }

  addKeyword(keyword: Keyword){
    this.keywordService.addKeywordSelection(this.extractFittingKeywordValue(keyword));
  }

  openDocument(){
    this.router.navigate(['/document', this.publication?.publication_id]);
  }

  openDocumentInNewTab(){
    const url = this.router.serializeUrl(
      this.router.createUrlTree(['/document', this.publication?.publication_id])
    );

    window.open(url, '_blank');
  }


}
