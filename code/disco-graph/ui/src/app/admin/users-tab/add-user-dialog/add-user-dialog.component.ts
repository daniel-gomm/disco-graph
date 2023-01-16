import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-add-user-dialog',
  templateUrl: './add-user-dialog.component.html',
  styleUrls: ['./add-user-dialog.component.scss']
})
export class AddUserDialogComponent {

  hidePassword: boolean = true;
  errorMessage: string = '';

  username: string = '';
  password: string = '';

  constructor (
    private userService: UserService,
    private dialogRef: MatDialogRef<AddUserDialogComponent>
  ) {}

  registerUser(): void {
    if (!(this.username && this.password)){
      this.errorMessage = 'Please provide username and password.';
      return;
    }
    this.userService.createUser(this.username, this.password)
    .subscribe({
      error: (error: HttpErrorResponse) => {
        this.errorMessage = 'Failed to create user ' + this.username;
      },
      complete: () => {
        this.dialogRef.close(true);
      }
    })
  }

  close() {
    this.dialogRef.close(false);
  }

}
