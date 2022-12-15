import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { finalize, tap } from 'rxjs';
import { DeleteDialogComponent } from 'src/app/components/dialogs/delete-dialog/delete-dialog.component';
import { User } from 'src/app/model/user';
import { UserService } from 'src/app/services/user.service';
import { AddUserDialogComponent } from './add-user-dialog/add-user-dialog.component';

@Component({
  selector: 'app-users-tab',
  templateUrl: './users-tab.component.html',
  styleUrls: ['./users-tab.component.scss']
})
export class UsersTabComponent implements OnInit {

  snackBarConfig: MatSnackBarConfig = {
    duration: 4000,
  }

  USER_LOADING_LIMIT = 20;
  INITIAL_USER_LOADING_LIMIT = 40;
  nextPageToLoad: number = 1;
  users: User[] = [];
  loadingUsers: boolean = true;
  lastResultSize: number = 0;

  constructor (
    private userService: UserService,
    private dialog: MatDialog,
    private _snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadingUsers = true;
    this.userService
      .getUsers(this.nextPageToLoad, this.INITIAL_USER_LOADING_LIMIT)
      .pipe(
        finalize(() => {
          this.loadingUsers = false;
        })
      )
      .subscribe((users: User[]) => {
        this.users = users;
        this.lastResultSize = users.length;
      });
  }

  onScroll():void {
    if(this.lastResultSize = 0){
      //No more users to load
      return;
    }
    this.loadingUsers = true;
    this.userService
    .getUsers(++this.nextPageToLoad, this.USER_LOADING_LIMIT)
    .pipe(
      finalize(() => {
        this.loadingUsers = false;
      })
    )
    .subscribe((users: User[]) => {
      this.users.push(...users);
      this.lastResultSize = users.length;
    });
  }

  createUser(){
    this.dialog.open(AddUserDialogComponent)
    .afterClosed()
    .subscribe((creationSuccessful) => {
      if(creationSuccessful){
        this.openSnackBar('Successfully created new user.');
      }
    })
  }

  deleteUser(username: string){
    this.dialog.open(DeleteDialogComponent)
    .afterClosed()
    .subscribe((deletionConfirmed) => {
      if(deletionConfirmed){
        this.userService.deleteUser(username)
        .subscribe({
          error: (error: HttpErrorResponse) => {
            this.openSnackBar('Failed to delete user.');
          },
          complete: () => {
            this.openSnackBar(`Deleted ${username}`);
            this.users = this.users.filter(user => user.username !== username);
          }
        });
      }
    })
  }

  openSnackBar(message: string){
    this._snackBar.open(message, 'Dismiss', this.snackBarConfig);
  }

}
