import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-user-login',
  templateUrl: './user-login.component.html',
  styleUrls: ['./user-login.component.scss']
})
export class UserLoginComponent {

  @ViewChild('passwordInput') passwordInput!: ElementRef<HTMLInputElement>;
  @ViewChild('usernameInput') usernameInput!: ElementRef<HTMLInputElement>;

  hidePassword: boolean = true;
  errorMessage: string = '';
  loginSuccessful: boolean = false;

  username: string = '';
  password: string = '';

  constructor(
    private authServie: AuthenticationService
  ) {}


  login(){
    if (!(this.username && this.password)){
      this.errorMessage = 'Please provide username and password.';
      return;
    }
    this.authServie.login_user(this.username, this.password).subscribe({
      error: (error: HttpErrorResponse) => {
        this.errorMessage = this.authServie.getLoginErrorMessage(error);
      },
      complete: () => {
        this.authServie.loggedInUser = this.username;
        this.loginSuccessful = true;
      }
    });
  }
}
