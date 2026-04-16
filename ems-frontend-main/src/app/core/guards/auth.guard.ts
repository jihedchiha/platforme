import { inject } from '@angular/core'
import { CanActivateFn, Router } from '@angular/router'
import { AuthService } from '../services/auth.service'

// ── Guard : utilisateur connecté ──────────────────
export const authGuard: CanActivateFn = () => {
  const auth   = inject(AuthService)
  const router = inject(Router)

  if (auth.isLoggedIn()) return true

  router.navigate(['/'])
  return false
}

// ── Guard : admin seulement ───────────────────────
export const adminGuard: CanActivateFn = () => {
  const auth   = inject(AuthService)
  const router = inject(Router)

  if (auth.isAdmin()) return true

  if (auth.isLoggedIn()) {
    if (auth.isSuperAdmin()) router.navigate(['/salles']);
    else                     router.navigate(['/dashboard']);
  } else {
    router.navigate(['/']);
  }

  return false
}

// ── Guard : redirige si déjà connecté ────────────
export const guestGuard: CanActivateFn = () => {
  const auth   = inject(AuthService)
  const router = inject(Router)

  if (!auth.isLoggedIn()) return true

  if (auth.isSuperAdmin()) {
    router.navigate(['/salles']);
  } else {
    router.navigate(['/dashboard']);
  }
  return false
}