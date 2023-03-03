import { transition } from '@angular/animations';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { debounceTime, distinctUntilChanged, finalize, Observable, startWith, switchMap } from 'rxjs';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';
import { DocumentService } from 'src/app/services/document.service';
import { KeywordService } from 'src/app/services/keyword.service';

@Component({
  selector: 'app-add-keyword-dialog',
  templateUrl: './add-keyword-dialog.component.html',
  styleUrls: ['./add-keyword-dialog.component.scss']
})
export class AddKeywordDialogComponent {

  languages$!: Observable<string[]>
  loadingFailed: boolean = false;
  inputControl = new FormControl('');
  loading: boolean = false;
  inputDisabled: boolean = false;
  selectedLanguage!: string;
  languageSelectDisabled: boolean = true;
  translations: ValueWithLanguage[] = [];


  document!:Publication;

  @ViewChild('keywordInput') keywordInput!: ElementRef<HTMLInputElement>;
  @ViewChild('languageSelect') languageSelect!: MatSelect;

  constructor(
    private documentService: DocumentService,
    private keywordService: KeywordService,
    public dialogRef: MatDialogRef<AddKeywordDialogComponent>
  ) {}

  ngOnInit(): void {
    this.languages$ = this.keywordService.getLanguages();
    this.languages$.subscribe({
      error: (e:HttpErrorResponse) => {
        this.loadingFailed = true;
      },
      next: (langs: string[]) => {
        this.initiateTranslations(langs);
      },
    });
    this.inputControl.valueChanges.pipe(
      startWith(null),
      distinctUntilChanged(),
      debounceTime(250),
      switchMap(value => this.getAutocompleteSugesstions(value)
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

  addKeyword(keyword:Keyword): void {
    this.documentService.addKeyword(this.document, keyword).subscribe({
      error: (e:HttpErrorResponse) => {
        this.loadingFailed = true;
      },
      complete: () => {
        this.dialogRef.close(true);
      }
    });
    this.dialogRef.close(true);
    this.document.keywords?.push(keyword);
  }

  getAutocompleteSugesstions(startKeys: string | null): Observable<ValueWithLanguage[]> {
    this.loading = true;
    return this.keywordService.getAutocompleteSuggestion(startKeys);
  }

  getFilteredKeywords(): ValueWithLanguage[]{
    return this.keywordService.filteredKeywords;
  }

  initiateTranslations(languages: string[]) {
    this.translations = [];
    for (const lang of languages){
      this.translations.push({
        value: '',
        language: lang
      })
    }
  }

  filterTranslations(languages: string[]): void {
    this.initiateTranslations(languages);
    this.translations = this.translations.filter(translation => translation.language !== this.selectedLanguage);
  }

  selectKeyword(event: MatAutocompleteSelectedEvent): void {
    const selectedKeyword: ValueWithLanguage | undefined = this.keywordService.filteredKeywords.find(keyword => keyword.value === event.option.viewValue);
    if(selectedKeyword){
      this.inputControl.setValue(selectedKeyword.value);
      this.inputControl.disable();
      this.inputDisabled = true;
      this.selectedLanguage = selectedKeyword.language;
      this.translations = [];
      this.languageSelectDisabled = true;
    } else {
      this.inputControl.setValue(null);
    }
  }

  selectLanguage(languages: string[]): void {
    this.filterTranslations(languages);
    this.languageSelectDisabled = true;
  }

  keydown(event: KeyboardEvent){
    if(event.key === "Enter"){
      this.languageSelect.setDisabledState(false);
      this.inputControl.disable();
      this.inputDisabled = true;
    }
  }

  cancel(): void {
    this.dialogRef.close(false);
  }

  add(): void {
    let keyword: Keyword = {
      values: [],
      verification_status: 0,
    }
    let main_val = this.inputControl.value;
    if (main_val && this.selectedLanguage){
      this.translations.push({
        value: main_val,
        language: this.selectedLanguage
      });
      keyword.values = this.translations.filter(trans => trans.value !== '');
      this.addKeyword(keyword)
    }
  }

}
