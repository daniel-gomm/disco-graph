import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-user-login',
  templateUrl: './user-login.component.html',
  styleUrls: ['./user-login.component.scss']
})
export class UserLoginComponent {

  hidePassword: boolean = true;
  errorMessage: string = '';

  username: string = '';
  password: string = '';

  constructor(
    private authService: AuthenticationService,
    public dialogRef: MatDialogRef<UserLoginComponent>
  ) {}


  login(){
    if (!(this.username && this.password)){
      this.errorMessage = 'Please provide username and password.';
      return;
    }
    this.authService.login_user(this.username, this.password).subscribe({
      error: (error: HttpErrorResponse) => {
        this.errorMessage = this.authService.getLoginErrorMessage(error);
      },
      complete: () => {
        this.dialogRef.close(true);
      }
    });
  }

  closeWithoutLogin() {
    this.dialogRef.close(false);
  }
}
