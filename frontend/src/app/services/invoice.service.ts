import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpService } from './http-client.service';

@Injectable({
  providedIn: 'root'
})
export class InvoiceService {

  private apiBaseUrl = 'http://localhost:8000';   

  constructor(private http: HttpService) {}

  uploadZip(file: File): Observable<{ download: string }> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.postFormData<{ download: string }>(
      `${this.apiBaseUrl}/process_zip/`,
      formData
    );
  }


  //TODO(martin): example of a service that uses the HttpService
//   getUserList(): Observable<any[]> {
//     return this.http.get<any[]>('https://api.example.com/users');
//   }

//   createUser(user: Partial<any>): Observable<any> {
//     return this.http.post<any>('https://api.example.com/users', user);
//   }

//   updateUser(id: string, user: Partial<any>): Observable<any> {
//     return this.http.put<any>(`https://api.example.com/users/${id}`, user);
//   }
}
