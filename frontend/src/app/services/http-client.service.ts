import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private defaultHeaders = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  get<T>(url: string, params?: { [key: string]: string | number }): Observable<T> {
    const httpParams = new HttpParams({ fromObject: params ?? {} });
    return this.http.get<T>(url, {
      headers: this.defaultHeaders,
      params: httpParams
    });
  }

  post<T, B = any>(url: string, body: B): Observable<T> {
    return this.http.post<T>(url, body, {
      headers: this.defaultHeaders
    });
  }

  put<T, B = any>(url: string, body: B): Observable<T> {
    return this.http.put<T>(url, body, {
      headers: this.defaultHeaders
    });
  }

  postFormData<T>(url: string, formData: FormData): Observable<T> {
    return this.http.post<T>(url, formData); // No headers necesarios: el navegador lo maneja automáticamente
  }
  

}
