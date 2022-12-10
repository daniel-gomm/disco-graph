import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { KeywordInputComponent } from './components/keyword-input/keyword-input.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MaterialDesignModule} from './modules/material-design/material-design.module'
import { HttpClientModule } from "@angular/common/http";
import { ResultsComponent } from './components/results/results.component';
import { KeywordSuggestionComponent } from './components/keyword-suggestion/keyword-suggestion.component';
import { SearchInputComponent } from './components/search-input/search-input.component';
import { ResultItemComponent } from './components/result-item/result-item.component';
import { FilterPaneComponent } from './components/filter-pane/filter-pane.component';
import { YearsFilterComponent } from './components/years-filter/years-filter.component';
import { FooterComponent } from './components/footer/footer.component';
import { AttributeFilterComponent } from './components/attribute-filter/attribute-filter.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    KeywordInputComponent,
    ResultsComponent,
    KeywordSuggestionComponent,
    SearchInputComponent,
    ResultItemComponent,
    FilterPaneComponent,
    YearsFilterComponent,
    FooterComponent,
    AttributeFilterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialDesignModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FontAwesomeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
