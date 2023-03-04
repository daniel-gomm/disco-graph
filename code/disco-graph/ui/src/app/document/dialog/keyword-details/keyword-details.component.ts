import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Keyword } from 'src/app/model/publication';

@Component({
  selector: 'app-keyword-details',
  templateUrl: './keyword-details.component.html',
  styleUrls: ['./keyword-details.component.scss']
})
export class KeywordDetailsComponent {

  keyword: Keyword;
  displayedColumns = ['language', 'value'];

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: Keyword
  ) {
    this.keyword = data;
  }

}
