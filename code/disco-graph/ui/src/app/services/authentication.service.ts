import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  loggedInUser: string = '';

  constructor(
    private http: HttpClient,
  ) { }

  login_user(username: string, password: string): Observable<any>{
    return this.http.post('/auth/user/login', {
      username: username,
      password: password
    },
    {responseType: 'text'});
  }

  login_admin(username: string, password: string): Observable<any>{
    return this.http.post('/auth/admin/login', {
      username: username,
      password: password
    },
    {responseType: 'text'});
  }

  register_user(username:string, password: string): Observable<any>{
    return this.http.post('/auth/user/register', {
      username: username,
      password: password
    },
    {responseType: 'text'});
  }

  logout(): Observable<any> {
    return this.http.post('/auth/logout', {}, {responseType: 'text'});
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

}
