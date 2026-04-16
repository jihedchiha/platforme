import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Salle } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class SalleService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/salles/`;

  /** Liste toutes les salles (Admin uniquement) */
  getSalles(): Observable<Salle[]> {
    return this.http.get<Salle[]>(this.baseUrl);
  }

  /** Récupère une salle par son ID */
  getSalle(id: string): Observable<Salle> {
    return this.http.get<Salle>(`${this.baseUrl}${id}/`);
  }

  /** Crée une nouvelle salle */
  createSalle(data: FormData): Observable<Salle> {
    return this.http.post<Salle>(this.baseUrl, data);
  }

  /** Modifie une salle existante */
  updateSalle(id: string, data: FormData): Observable<Salle> {
    return this.http.put<Salle>(`${this.baseUrl}${id}/`, data);
  }

  /** Supprime une salle */
  deleteSalle(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}${id}/`);
  }

  /** Récupère la configuration de branding de la salle active */
  getConfig(): Observable<{ couleur_primaire: string, couleur_secondaire: string }> {
    return this.http.get<{ couleur_primaire: string, couleur_secondaire: string }>(`${this.baseUrl}config/`);
  }
}
