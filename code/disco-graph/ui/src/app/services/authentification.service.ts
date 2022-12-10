import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthentificationService {

  constructor(
    private http: HttpClient,
  ) { }

  login_user(username: string, password: string): Observable<any>{
    return this.http.post('/auth/user/login', {
      username: username,
      password: password
    })
  }

  login_admin(username: string, password: string): Observable<any>{
    return this.http.post('/auth/admin/login', {
      username: username,
      password: password
    })
  }

  register_user(username:string, password: string): Observable<any>{
    return this.http.post('/auth/user/register', {
      username: username,
      password: password
    })
  }

  logout(): Observable<any> {
    return this.http.post('/auth/logout')
  }

}
