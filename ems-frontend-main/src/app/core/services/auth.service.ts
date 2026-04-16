import { Injectable, inject, signal } from '@angular/core'
import { Router } from '@angular/router'
import { ApiService } from './api.service'
import { tap } from 'rxjs/operators'
import { Observable } from 'rxjs'

export interface Salle {
  id: string
  nom: string
  slug: string
  logo?: string | null
  couleur?: string | null
  couleur_secondaire?: string | null
  pack_saas: 'starter' | 'pro' | 'enterprise'
  features_actives: string[]
  actif: boolean
}

export interface AuthUser {
  id    : string
  role  : 'superadmin' | 'admin' | 'personnel'
  username: string
  nom?    : string
  email?  : string
  salles? : Salle[]
}

@Injectable({ providedIn: 'root' })
export class AuthService {

  private router     = inject(Router)
  private apiService = inject(ApiService)

  // -- Signaux pour la réactivité
  user = signal<AuthUser | null>(this.getUser());
  activeSalleId = signal<string | null>(localStorage.getItem('selectedSalleId'));

  // ── Getters ──────────────────────────────────────

  getToken(): string | null {
    return localStorage.getItem('access')
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh')
  }

  getUser(): AuthUser | null {
    const raw = localStorage.getItem('user')
    if (!raw) return null
    try   { return JSON.parse(raw) as AuthUser }
    catch { return null }
  }

  getRole(): string {
    return this.user()?.role || ''
  }

  isLoggedIn(): boolean {
    return !!this.user();
  }

  isSuperAdmin(): boolean {
    return this.user()?.role === 'superadmin'
  }

  isAdmin(): boolean {
    return this.user()?.role === 'admin'
  }

  isPersonnel(): boolean {
    return this.getRole() === 'personnel'
  }

  // ── Login ──────────────────────────────────────

  login(username: string, password: string): Observable<any> {
    return this.apiService.login(username, password).pipe(
      tap((res: any) => {
        localStorage.setItem('access',  res.access)
        localStorage.setItem('refresh', res.refresh)
        localStorage.setItem('user',    JSON.stringify(res.user))
        this.user.set(res.user);
        
        // Sélectionner la première salle par défaut si non définie
        if (res.user.salles && res.user.salles.length > 0) {
          this.setSelectedSalle(res.user.salles[0].id)
        }
      })
    )
  }

  setSelectedSalle(id: string | null): void {
    if (id) {
      localStorage.setItem('selectedSalleId', id)
    } else {
      localStorage.removeItem('selectedSalleId')
    }
    this.activeSalleId.set(id)
  }

  getActiveSalle(): Salle | null {
    const user = this.getUser()
    if (!user || !user.salles) return null
    return user.salles.find(s => s.id === this.activeSalleId()) || null
  }

  // ── Logout ──────────────────────────────────────

  logout(): void {
    const refresh = this.getRefreshToken()
    if (refresh) {
      this.apiService.logout(refresh).subscribe({ error: () => {} })
    }
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
    this.user.set(null);
    this.setSelectedSalle(null)
    this.router.navigate(['/'])
  }

  // ── Redirection après login selon rôle ──────────

  redirectAfterLogin(): void {
    const role = this.getRole()
    if (role === 'superadmin') {
      this.router.navigate(['/salles'])
    } else if (role === 'admin' || role === 'personnel') {
      this.router.navigate(['/dashboard'])
    } else {
      this.router.navigate(['/'])
    }
  }
}