import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SearchRoutingModule } from './search-routing.module';
import { AttributeFilterComponent } from './filters/attribute-filter/attribute-filter.component';
import { FilterPaneComponent } from './filters/filter-pane/filter-pane.component';
import { YearsFilterComponent } from './filters/years-filter/years-filter.component';
import { KeywordInputComponent } from './input/keyword-input/keyword-input.component';
import { SearchInputComponent } from './input/search-input/search-input.component';
import { ResultItemComponent } from './result/result-item/result-item.component';
import { ResultsComponent } from './result/results/results.component';
import { SearchComponent } from './search/search.component';
import { KeywordSuggestionComponent } from './suggestion/keyword-suggestion/keyword-suggestion.component';
import { MaterialDesignModule } from '../modules/material-design/material-design.module';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';


@NgModule({
  declarations: [
    AttributeFilterComponent,
    FilterPaneComponent,
    YearsFilterComponent,
    KeywordInputComponent,
    SearchInputComponent,
    ResultItemComponent,
    ResultsComponent,
    SearchComponent,
    KeywordSuggestionComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialDesignModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FontAwesomeModule,
    CommonModule,
    MaterialDesignModule,
    SearchRoutingModule
  ]
})
export class SearchModule { }
