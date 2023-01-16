import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent {

  hidePassword: boolean = true;
  errorMessage: string = '';

  username: string = '';
  password: string = '';

  constructor (
    private authService: AuthenticationService
  ) {}

  adminLoggedIn(): boolean{
    return this.authService.isAdminLoggedIn();
  }

}
