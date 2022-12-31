import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../model/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private http: HttpClient
  ) { }

  getUsers(page: number, keys: string = '', limit: number = 20): Observable<User[]> {
    return this.http.get<User[]>(`/user?limit=${limit}&page=${page}${keys === '' ? '' : '&keys=' + keys}`);
  }

  deleteUser(username: string): Observable<any> {
    return this.http.delete(`/user/${username}`, {responseType: 'text'});
  }

  createUser(username: string, password: string): Observable<any>{
    return this.http.post(`/user/${username}`, 
    {password: password},
    {responseType: 'text'});
  }

}
