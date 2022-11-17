import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import {FormControl} from '@angular/forms';
import {MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {MatChipInputEvent} from '@angular/material/chips';
import {Observable, of} from 'rxjs';
import {map, startWith} from 'rxjs/operators';

@Component({
  selector: 'app-keyword-input',
  templateUrl: './keyword-input.component.html',
  styleUrls: ['./keyword-input.component.less']
})
export class KeywordInputComponent implements OnInit {

  separatorKeysCodes: number[] = [ENTER, COMMA];
  keywordControl = new FormControl('')
  filteredKeywords: Observable<string[]>;
  keywords: string[] = [];
  allKeywords: string[] = ['Herstellung', 'Qualitätssicherung', 'Prognosemodell', 'Wandlungstreiber', 'Szenarien', 'Simulation'];
  keywordSuggestions: string[] = ["Produktallokation", "Produktionsnetzwerk"];
  filteredKeywordSuggestions : Observable<string[]>;

  @ViewChild('keywordInput') keywordInput!: ElementRef<HTMLInputElement>;

  constructor() { 
    this.filteredKeywords = this.keywordControl.valueChanges.pipe(
      startWith(null),
      map((keyword: string | null) => 
      (keyword ? this._filter(keyword) : this.allKeywords.slice()))
    );
    this.filteredKeywordSuggestions = of(this.keywordSuggestions);
  }

  ngOnInit(): void {
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

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.allKeywords.filter(keyword => keyword.toLowerCase().includes(filterValue));
  }

  removeSuggestion(keywordSuggestion: string): void {
    const index = this.keywordSuggestions.indexOf(keywordSuggestion);

    if (index >= 0) {
      this.keywordSuggestions.splice(index, 1);
    }
    this.keywords.push(keywordSuggestion)
  }

}
