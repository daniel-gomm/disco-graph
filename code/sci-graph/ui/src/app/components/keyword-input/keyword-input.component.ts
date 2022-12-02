import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import {FormControl} from '@angular/forms';
import {MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatChipInputEvent} from '@angular/material/chips';
import {Observable, of} from 'rxjs';
import {map, startWith, filter, distinctUntilChanged, debounceTime, tap, switchMap, finalize} from 'rxjs/operators';
import {ValueWithLanguage} from '../../model/publication';
import { HttpClient } from '@angular/common/http';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-keyword-input',
  templateUrl: './keyword-input.component.html',
  styleUrls: ['./keyword-input.component.less']
})
export class KeywordInputComponent implements OnInit {

  separatorKeysCodes: number[] = [ENTER, COMMA];
  keywordControl = new FormControl('');
  filteredKeywords: ValueWithLanguage[] = [];
  loading: boolean = true;
  keywords: string[] = [];
  keywordSuggestions: string[] = ["Produktallokation", "Produktionsnetzwerk"];
  //filteredKeywordSuggestions : Observable<string[]>;
  suggestionLimit: number = 10;

  cachedPreviousInput: string = "";


  @ViewChild('keywordInput') keywordInput!: ElementRef<HTMLInputElement>;

  constructor(
    private keywordService: KeywordService,
  ) { 
  }

  ngOnInit(): void {
    this.keywordControl.valueChanges.pipe(
      filter(res => {
        return res !== null && res.length >= 1;
      }),
      startWith(null),
      distinctUntilChanged(),
      debounceTime(200),
      switchMap(value => this.loadKeywordSuggestions(value)
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      )
    )
    .subscribe((res: ValueWithLanguage[]) => {
      this.filteredKeywords = res;
      console.log(res);
    });
  }

  loadKeywordSuggestions(input: string | null): Observable<ValueWithLanguage[]> {
    if(input === null){
      input = "*";
    }
    if (input !== "*" && this.filteredKeywords.length < this.suggestionLimit && input.startsWith(this.cachedPreviousInput)){
      this.cachedPreviousInput = input;
      return of(this._filterCachedSuggestions(input))
    }
    this.cachedPreviousInput = input;
    return this.keywordService.getKeywords(input, this.suggestionLimit);
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add keyword
    if (value) {
      this.keywords.push(value);
    }

    // Clear the input value
    event.chipInput!.clear();

    this.keywordControl.setValue(null);
  }

  remove(keyword: string): void {
    const index = this.keywords.indexOf(keyword);

    if (index >= 0) {
      this.keywords.splice(index, 1);
    }
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    this.keywords.push(event.option.viewValue);
    this.keywordInput.nativeElement.value = '';
    this.keywordControl.setValue(null);
  }

  private _filterCachedSuggestions(inputValue: string): ValueWithLanguage[] {
    const filterValue = inputValue.toLowerCase();

    return this.filteredKeywords.filter(keyword => keyword.value.toLowerCase().includes(filterValue));
  }

  removeSuggestion(keywordSuggestion: string): void {
    const index = this.keywordSuggestions.indexOf(keywordSuggestion);

    if (index >= 0) {
      this.keywordSuggestions.splice(index, 1);
    }
    this.keywords.push(keywordSuggestion)
  }

}
