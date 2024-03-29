import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { Keyword, Publication, ValueWithLanguage } from 'src/app/model/publication';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { StatusService } from 'src/app/services/status.service';
import { AddKeywordDialogComponent } from '../../dialog/add-keyword-dialog/add-keyword-dialog.component';
import { KeywordDetailsComponent } from '../../dialog/keyword-details/keyword-details.component';

@Component({
  selector: 'app-document-overview',
  templateUrl: './document-overview.component.html',
  styleUrls: ['./document-overview.component.scss']
})
export class DocumentOverviewComponent {

  @Input() document!:Publication;

  DEFAULT_LANGUAGE = 'en';

  upvotedKeywords: Keyword[] = [];
  downvotedKeywords: Keyword[] = [];
  errorMessage: string = '';

  snackBarConfig: MatSnackBarConfig = {
    duration: 4000,
  }

  constructor (
    private statusService: StatusService,
    private authService: AuthenticationService,
    public dialog: MatDialog,
    private _snackBar: MatSnackBar,
  ) { }


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

  isLoggedIn(): boolean {
    return this.authService.isUserLoggedIn();
  }

  keywordUpdateStatus(keyword: Keyword): number {
    //return 0 if the keywords verification status has not been updated, -1 if it has been downvoted and 1 if if it has been upvoted
    let comparisionResult = (-this.downvotedKeywords.indexOf(keyword)) + this.upvotedKeywords.indexOf(keyword);
    return comparisionResult/Math.max(1, Math.abs(comparisionResult));
  }

  upvoteKeyword(keyword: Keyword): void{
    this.statusService.updateKeywordVerification(this.document.publication_id, this.extractValueInPublicationLanguage(keyword).value, keyword.verification_status + 1)
    .subscribe({
      complete: () => {
        this.errorMessage ='';
        this.upvotedKeywords.push(keyword);
      },
      error: (e: HttpErrorResponse) => this.errorMessage = `Could not update the status. Error ${e.status}: ${e.statusText}`
    });
  }

  downvoteKeyword(keyword: Keyword): void{
    this.statusService.updateKeywordVerification(this.document.publication_id, this.extractValueInPublicationLanguage(keyword).value, keyword.verification_status - 1)
    .subscribe({
      complete: () => {
        this.errorMessage ='';
        this.downvotedKeywords.push(keyword);
      },
      error: (e: HttpErrorResponse) => this.errorMessage = `Could not update the status. Error ${e.status}: ${e.statusText}`
    });;
  }

  rollbackUpvoteKeyword(keyword: Keyword): void {
    this.statusService.updateKeywordVerification(this.document.publication_id, this.extractValueInPublicationLanguage(keyword).value, keyword.verification_status - 1)
    .subscribe({
      complete: () => {
        this.errorMessage ='';
        this.upvotedKeywords = this.upvotedKeywords.filter(kw => kw !== keyword);
      },
      error: (e: HttpErrorResponse) => this.errorMessage = `Could not update the status. Error ${e.status}: ${e.statusText}`
    });;
  }

  rollbackDownvoteKeyword(keyword: Keyword): void {
    this.statusService.updateKeywordVerification(this.document.publication_id, this.extractValueInPublicationLanguage(keyword).value, keyword.verification_status + 1)
    .subscribe({
      complete: () => {
        this.errorMessage ='';
        this.downvotedKeywords = this.downvotedKeywords.filter(kw => kw !== keyword);
      },
      error: (e: HttpErrorResponse) => this.errorMessage = `Could not update the status. Error ${e.status}: ${e.statusText}`
    });;
  }

  openDocumentWebsite(){
    window.open(this.document.website, '_blank');
  }

  openKeywordDialog(){
    const dialogRef = this.dialog.open(AddKeywordDialogComponent);
    dialogRef.componentInstance.document = this.document;
    dialogRef.afterClosed().subscribe(keywordAdded => {
      if(keywordAdded){
        this.openSnackBar('Successfully added Keyword.')
      }
    });
  }

  openKeywordInfoDialog(keyword: Keyword): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = keyword;
    this.dialog.open(KeywordDetailsComponent, dialogConfig);
  }

  openSnackBar(message: string){
    this._snackBar.open(message, 'Dismiss', this.snackBarConfig);
  }

  hasValidURL(): boolean {
    if (!this.document.website){
      return false;
    }
    var pattern = new RegExp('^(https?:\\/\\/)?'+
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+
      '((\\d{1,3}\\.){3}\\d{1,3}))'+
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+
      '(\\?[;&a-z\\d%_.~+=-]*)?'+
      '(\\#[-a-z\\d_]*)?$','i');
    return !!pattern.test(this.document.website);
  }

}
