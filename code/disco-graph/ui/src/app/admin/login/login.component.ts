import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  hidePassword: boolean = true;
  errorMessage: string = '';

  username: string = '';
  password: string = '';

  constructor (
    private authService: AuthenticationService
  ) {}

  login(){
    if (!(this.username && this.password)){
      this.errorMessage = 'Please provide admin username and password.';
      return;
    }
    this.authService.login_admin(this.username, this.password).subscribe({
      error: (error: HttpErrorResponse) => {
        this.errorMessage = this.authService.getLoginErrorMessage(error);
      },
      complete: () => {
        this.errorMessage = "Successfully logged in!";
      }
    });
  }

}
