import { Component, Input } from '@angular/core';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';

@Component({
  selector: 'app-document-overview',
  templateUrl: './document-overview.component.html',
  styleUrls: ['./document-overview.component.scss']
})
export class DocumentOverviewComponent {

  @Input() document!:Publication;

  DEFAULT_LANGUAGE = 'en';


  extractKeywordsInPublicationLanguage(): ValueWithLanguage[] {
    let keywords: ValueWithLanguage[] = [];
    this.document.keywords?.forEach((kw) => {
      const val = kw.values.find((value) => value.language === this.document.language);
      if (val){
        keywords.push(val);
      }
    });
    return keywords;
  }

  extractValueInPublicationLanguage(keyword: Keyword): ValueWithLanguage {
    let val = keyword.values.find((value) => value.language === this.document.language);
    if(val) {
      return val;
    }
    val = keyword.values.find((value) => value.language === this.DEFAULT_LANGUAGE);
    if(val){
      return val;
    }
    throw new Error(`Unable to extract the matching keyword value from: ${keyword}`);
  }

}
