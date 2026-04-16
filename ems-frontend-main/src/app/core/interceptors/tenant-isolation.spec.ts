import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './auth.interceptor';
import { AuthService } from '../services/auth.service';

describe('Tenant Isolation (HttpInterceptor)', () => {
  let httpMock: HttpTestingController;
  let httpClient: HttpClient;
  let authService: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([authInterceptor])),
        provideHttpClientTesting(),
        AuthService
      ]
    });

    httpMock = TestBed.inject(HttpTestingController);
    httpClient = TestBed.inject(HttpClient);
    authService = TestBed.inject(AuthService);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should add X-Tenant-ID header when a salle is selected', () => {
    // 1. Simuler une salle sélectionnée
    authService.setSelectedSalle('salle-123');

    // 2. Faire une requête
    httpClient.get('/api/test').subscribe();

    // 3. Vérifier le header
    const req = httpMock.expectOne('/api/test');
    expect(req.request.headers.has('X-Tenant-ID')).toBe(true);
    expect(req.request.headers.get('X-Tenant-ID')).toBe('salle-123');
  });

  it('should NOT add X-Tenant-ID header when no salle is selected', () => {
    authService.setSelectedSalle(null);

    httpClient.get('/api/test').subscribe();

    const req = httpMock.expectOne('/api/test');
    expect(req.request.headers.has('X-Tenant-ID')).toBe(false);
  });

  it('should NOT add headers on login requests', () => {
    authService.setSelectedSalle('salle-123');

    httpClient.post('/api/users/login/', {}).subscribe();

    const req = httpMock.expectOne('/api/users/login/');
    expect(req.request.headers.has('X-Tenant-ID')).toBe(false);
    expect(req.request.headers.has('Authorization')).toBe(false);
  });
});
