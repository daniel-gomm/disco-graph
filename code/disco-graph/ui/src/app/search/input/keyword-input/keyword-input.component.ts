import { COMMA, ENTER}  from '@angular/cdk/keycodes';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';
import { startWith, filter, distinctUntilChanged, debounceTime, switchMap, finalize } from 'rxjs/operators';
import { ValueWithLanguage } from '../../../model/publication';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-keyword-input',
  templateUrl: './keyword-input.component.html',
  styleUrls: ['./keyword-input.component.scss']
})
export class KeywordInputComponent implements OnInit {

  separatorKeysCodes: number[] = [ENTER, COMMA];
  keywordControl = new FormControl('');
  loading: boolean = true;
  deleteLastKeyword: boolean = false;
  suggestionLimit: number = 10;


  @ViewChild('keywordInput') keywordInput!: ElementRef<HTMLInputElement>;

  constructor(
    private keywordService: KeywordService,
  ) { 
  }

  ngOnInit(): void {
    this.keywordControl.valueChanges.pipe(
      startWith(null),
      distinctUntilChanged(),
      debounceTime(250),
      switchMap(value => this.keywordService.getAutocompleteSuggestion(value)
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      )
    )
    .subscribe((res: ValueWithLanguage[]) => {
      this.keywordService.filteredKeywords = res;
    });
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    //Add keyword
    if (value){
      this.keywordService.filteredKeywords.forEach(keyword => {
        if (keyword.value === value){
          this.keywordService.addKeywordSelection(keyword);
          this.keywordService.filteredKeywords = [];
        }
      });
    }

    // Clear the input value
    event.chipInput!.clear();

    this.keywordControl.setValue(null);
  }

  remove(keyword: ValueWithLanguage): void {
    this.keywordService.removeKeywordSelection(keyword);
    // const index = this.keywordService.selectedKeywords.indexOf(keyword);
    // if(index >= 0){
    //   this.keywordService.selectedKeywords.splice(index, 1);
    // }
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const selectedKeyword: any = this.keywordService.filteredKeywords.find(keyword => keyword.value === event.option.viewValue);
    if(selectedKeyword){
      this.keywordService.addKeywordSelection(selectedKeyword);
      //this.keywordService.selectedKeywords.push(selectedKeyword);
    }
    this.keywordInput.nativeElement.value = '';
    this.keywordControl.setValue(null);
  }

  getSelectedKeywords(): ValueWithLanguage[]{
    return this.keywordService.selectedKeywords;
  }

  getFilteredKeywords(): ValueWithLanguage[]{
    return this.keywordService.filteredKeywords;
  }

  keydown(event: KeyboardEvent){
    if (!this.keywordControl.value && event.key === "Backspace"){
      if(this.deleteLastKeyword){
        let kwToRemove = this.keywordService.selectedKeywords.at(-1);
        if(kwToRemove){
          this.keywordService.removeKeywordSelection(kwToRemove);
        }
        this.deleteLastKeyword = false;
        return;
      } else {
        this.deleteLastKeyword = true;
        return;
      }
    }
    this.deleteLastKeyword = false;
  }

}
