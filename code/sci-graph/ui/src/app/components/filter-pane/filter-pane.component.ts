import { Component, Input, OnInit } from '@angular/core';
import { AttributeResponse } from 'src/app/model/responses';
import { FilterService } from 'src/app/services/filter.service';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-filter-pane',
  templateUrl: './filter-pane.component.html',
  styleUrls: ['./filter-pane.component.scss']
})
export class FilterPaneComponent implements OnInit {

  reloadButtonDisabled: boolean = true;
  attributesLoaded: boolean = false;
  attributes: AttributeResponse[] = []
  loadingError: boolean = false;

  constructor (
    private filterService: FilterService,
    private keywordService: KeywordService,
  ) {}


  ngOnInit(): void {
    this.filterService.getAttributes().subscribe({
      next: (value: AttributeResponse[]) => {
        this.attributes = value;
        this.attributesLoaded = true;
      },
      error: (e) => {
        this.attributesLoaded = true;
        this.loadingError = true;
      }
    })
  }

  enableReload(){
    this.reloadButtonDisabled = false;
  }
  
  disableReload(){
    this.reloadButtonDisabled = true;
  }

  reload(){
    this.keywordService.getResults();
    this.disableReload();
  }
}
