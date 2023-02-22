import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import { DocumentRoutingModule } from './document-routing.module';
import { DocumentComponent } from './document/document.component';
import { DocumentOverviewComponent } from './overview/document-overview/document-overview.component';
import { DocumentEditComponent } from './edit/document-edit/document-edit.component';
import { DocumentDetailsComponent } from './details/document-details/document-details.component';
import { MaterialDesignModule } from '../modules/material-design/material-design.module';
import { AddKeywordDialogComponent } from './dialog/add-keyword-dialog/add-keyword-dialog.component';


@NgModule({
  declarations: [
    DocumentComponent,
    DocumentOverviewComponent,
    DocumentEditComponent,
    DocumentDetailsComponent,
    AddKeywordDialogComponent
  ],
  imports: [
    CommonModule,
    MaterialDesignModule,
    DocumentRoutingModule,
    ReactiveFormsModule,
    FormsModule
  ]
})
export class DocumentModule { }
