// src/app/core/interceptors/auth.interceptor.ts
// ══════════════════════════════════════════════════════════════════
// Intercepteur Multi-Tenant — ajoute automatiquement le token Bearer
// ET le header X-Tenant-ID si une salle est sélectionnée
// ══════════════════════════════════════════════════════════════════

import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authService = inject(AuthService);

  // 1. Ne pas ajouter de headers sur le login
  const isLoginUrl = req.url.includes('/login/');
  if (isLoginUrl) {
    return next(req);
  }

  // 2. Récupérer les identifiants
  const token = authService.getToken();
  const tenantId = authService.activeSalleId();

  // 3. Cloner la requête avec les nouveaux headers
  const headers: { [name: string]: string } = {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (tenantId) {
    headers['X-Tenant-ID'] = tenantId;
  }

  const authReq = req.clone({ setHeaders: headers });

  // 4. Envoyer la requête et gérer l'expiration du token (401)
  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        console.warn('Session expirée ou non autorisée — redirection login');
        authService.logout(); // Utilise le logout centralisé
      }
      return throwError(() => error);
    })
  );
};