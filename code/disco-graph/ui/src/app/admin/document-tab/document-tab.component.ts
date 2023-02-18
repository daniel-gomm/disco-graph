import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { finalize } from 'rxjs';
import { DocumentTitleResponse } from 'src/app/model/responses';
import { DocumentService } from 'src/app/services/document.service';

@Component({
  selector: 'app-document-tab',
  templateUrl: './document-tab.component.html',
  styleUrls: ['./document-tab.component.scss']
})
export class DocumentTabComponent implements OnInit{


  DOCUMENT_LOADING_LIMIT = 10;
  INITIAL_DOCUMENT_LOADING_LIMIT = 40;
  nextPageToLoad = 1;
  lastResultSize: number = 0;
  documentTitles: DocumentTitleResponse[] = [];
  loadingDocuments: boolean = true;
  inputValue: string = '';
  currentSearchValue: string = '*';

  constructor (
    private documentService: DocumentService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadDocuments(this.INITIAL_DOCUMENT_LOADING_LIMIT);
  }

  search(): void {
    this.currentSearchValue = (this.inputValue === '' ? '*' : this.inputValue);
    this.documentTitles = [];
    this.nextPageToLoad = 1;
    this.lastResultSize = 0;
    this.loadDocuments(this.INITIAL_DOCUMENT_LOADING_LIMIT);
  }

  onScroll(): void{
    if(this.lastResultSize = 0){
      return;
    }
    this.loadDocuments(this.DOCUMENT_LOADING_LIMIT);
  }

  loadDocuments(limit: number = this.DOCUMENT_LOADING_LIMIT): void {
    this.loadingDocuments = true;
    this.documentService.getDocumentTitles(this.currentSearchValue, limit, this.nextPageToLoad++)
    .pipe(
      finalize(() => {
        this.loadingDocuments = false;
      })
    )
    .subscribe((documents: DocumentTitleResponse[]) => {
      this.documentTitles.push(...documents);
      this.lastResultSize = documents.length;
    })
  }

  showNotImplemented(): void {
    this.snackBar.open('This feature is not yet available.', 'Dismiss');
  }

}
