import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DocumentRoutingModule } from './document-routing.module';
import { DocumentComponent } from './document/document.component';
import { DocumentOverviewComponent } from './overview/document-overview/document-overview.component';
import { DocumentEditComponent } from './edit/document-edit/document-edit.component';
import { DocumentDetailsComponent } from './details/document-details/document-details.component';
import { MaterialDesignModule } from '../modules/material-design/material-design.module';


@NgModule({
  declarations: [
    DocumentComponent,
    DocumentOverviewComponent,
    DocumentEditComponent,
    DocumentDetailsComponent
  ],
  imports: [
    CommonModule,
    MaterialDesignModule,
    DocumentRoutingModule
  ]
})
export class DocumentModule { }
