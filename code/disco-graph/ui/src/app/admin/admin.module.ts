import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin/admin.component';
import { LoginComponent } from './login/login.component';
import { MaterialDesignModule } from '../modules/material-design/material-design.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InfiniteScrollModule } from 'ngx-infinite-scroll';
import { UsersTabComponent } from './users-tab/users-tab.component';
import { AddUserDialogComponent } from './users-tab/add-user-dialog/add-user-dialog.component';
import { DocumentTabComponent } from './document-tab/document-tab.component';


@NgModule({
  declarations: [
    AdminComponent,
    LoginComponent,
    UsersTabComponent,
    AddUserDialogComponent,
    DocumentTabComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    MaterialDesignModule,
    FormsModule,
    ReactiveFormsModule,
    InfiniteScrollModule
  ]
})
export class AdminModule { }
