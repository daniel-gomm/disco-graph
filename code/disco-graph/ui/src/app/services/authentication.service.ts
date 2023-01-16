import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { finalize, Observable, tap } from 'rxjs';
import { LoggedInUserRespone } from '../model/responses';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  loggedInUser: string = '';
  loggedInAdmin: string= '';

  constructor(
    private http: HttpClient,
  ) {
    //see if there is already a logged in user
    this.http.get<LoggedInUserRespone>('/auth/user').subscribe({
      next:(loggedInUser: LoggedInUserRespone) => {
          this.loggedInUser = loggedInUser.username;
      },
    }
      )
  }

  login_user(username: string, password: string): Observable<any>{
    return this.http.post('/auth/user/login', {
      username: username,
      password: password
    },
    {responseType: 'text'})
    .pipe(
      tap({
        complete: () => {
          this.loggedInUser = username;
        }
      })
    );
  }

  login_admin(username: string, password: string): Observable<any>{
    return this.http.post('/auth/admin/login', {
      username: username,
      password: password
    },
    {responseType: 'text'})
    .pipe(
      tap({
        complete: () => {
          this.loggedInAdmin = username;
        }
      })
    );
  }

  register_user(username:string, password: string): Observable<any>{
    return this.http.post('/auth/user/register', {
      username: username,
      password: password
    },
    {responseType: 'text'});
  }

  logout(): Observable<any> {
    return this.http.post('/auth/logout', {}, {responseType: 'text'})
    .pipe(
      tap({
        complete: () => {
          this.loggedInUser = '';
        }
      })
    );
  }

  getLoginErrorMessage(error: HttpErrorResponse): string{
    switch (error.status){
      case 403: {
        return 'Password or username incorrect.';
      }
      default: {
        return 'An error occured when trying to log you in.';
      }
    }
  }

  isUserLoggedIn(): boolean{
    return Boolean(this.loggedInUser);
  }

  isAdminLoggedIn(): boolean{
    return Boolean(this.loggedInAdmin);
  }

}
