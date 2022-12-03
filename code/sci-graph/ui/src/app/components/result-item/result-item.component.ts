import { Component, Input, OnInit } from '@angular/core';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';

@Component({
  selector: 'app-result-item',
  templateUrl: './result-item.component.html',
  styleUrls: ['./result-item.component.scss']
})
export class ResultItemComponent implements OnInit{

  @Input() publication: Publication | undefined = undefined;
  
  ngOnInit():void {

  }

  extractKeyword(keyword: Keyword): ValueWithLanguage{
    let value = keyword.values.at(0);
    if(value){
      return value;
    }
    return {value: '', language:'none'}
  }

}
